import urllib
import json
import pprint
import sys
import random
import base64
import requests
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.test
users = db.users
activities = db.activities
standards = db.standards
categories = db.categories


def addUser(user,password):
    if users.find_one({"username" : user}) != None:
        return False
    tmp = base64.b64encode(password)
    newuser = {"username" : user, "password" : tmp}
    users.insert(newuser)
    return True

def updateUserInfo(user,address,birthday,email,gender,name,phone,nickname):
    info={"address":address,"birthday":birthday,"email":email,"gender":gender,"name":name,"phone":str(phone),"nickname":nickname}
    for x in info:
        users.update({"username":user},{"$set":{x:info[x]}})
    return True

def updateUserDesire(user,string):
    users.update({"username":user},{"$set":{"desire":string}})
    return True

def updateActivities(user,data,catChain):
    print 'data: ',data
    catChain=deword('.'.join(catChain.split(',')))
    print "catChain: ",catChain
    for key in data:
        if data[key]['static']=='True':
            users.update({"username":user,"activity.actName":key},{"$set":{"activity.$.interest":data[key]['interest'],"activity.$.describe":data[key]['describe'],"activity.$.time":data[key]['times']}})
        else:
            #create new activity
            print 'new act: ',data[key]
            info={"interest":data[key]['interest'],"describe":data[key]['describe'],"time":data[key]['times'],"comment":[],"actName":key,"ability":data[key]['ability'],"category":data[key]['category']}
            users.update({"username":user},{"$push":{"activity":info}})
            categories.update({catChain:{'$exists':'true'}},{"$push":{catChain+'.items':user},"$inc":{catChain+'.number':1}})
    return True

def checkUserPass(user,password):
    encpass = base64.b64encode(password)
    tmp = users.find_one({"username" : user})
    if tmp == None:
        return 2
    #if encpass == tmp["password"]:
    if tmp["password"]==password:
        return True
    else:
        return False

def getUserAddress(username):
    info = users.find_one({"username":username})["address"]
    res = info['street']+ " "+info['city']+" "+ info['zipcode']
    return res

def getUserBirthday(username):
    info = users.find_one({"username":username})["birthday"]
    year=int(info)%10000
    day=int(info)%1000000/10000
    month=int(info)/1000000
    return "/".join(str(i) for i in [month,day,year])

def getUserEmail(username):
    info = users.find_one({"username":username})["email"]
    return info

def getUserGender(username):
    info = users.find_one({"username":username})["gender"]
    if info=="M":
        return "male"
    if info=="F":
        return "female"

def getUserName(username):
    info = users.find_one({"username":username})["name"]
    return info

def getUserNickname(username):
    info = users.find_one({"username":username})["nickname"]
    return info

def getUserPhone(username):
    info = users.find_one({"username":username})["phone"]
    x=info[0:3]
    y=info[3:-4]
    z=info[-4:]
    return "-".join([x,y,z])

def getUserFirstName(username):
    s=str.split(str(getUserName(username))," ")
    return s[0]

def getUserLastName(username):
    s=str.split(str(getUserName(username))," ")
    return s[1]

def getUserBirthMonth(username):
    info = users.find_one({"username":username})["birthday"]
    month=int(info/1000000)
    return month
    
def getUserBirthDay(username):
    info = users.find_one({"username":username})["birthday"]
    day=int(info%1000000/10000)
    return day

def getUserBirthYear(username):
    info = users.find_one({"username":username})["birthday"]
    year=int(info%10000)
    return year

def getUserAddressLine(username):
    info = users.find_one({"username":username})["address"]['street']
    return info

def getUserAddressCity(username):
    info = users.find_one({"username":username})["address"]['city']
    return info

def getUserAddressZip(username):
    info = users.find_one({"username":username})["address"]['zipcode']
    return info

def getUserDesire(username):
    info = users.find_one({"username":username})["desire"]
    return info

def getStandard(ageupper):
    ageupper=int(ageupper)
    info=standards.find({"age":ageupper})
    l=[]
    for i in info:
        l.append(i["standard"])
    return l

def getStandardRating(ageupper):
    ageupper=int(ageupper)
    info=standards.find({"age":ageupper})
    l=[]
    for i in info:
        l.append(i["standard"])
    return l

def getUserActivities(username):
    info = users.find_one({"username":username})["activity"]
    res=[]
    for activity in info:
        act=activity["actName"]
        comment=activity["comment"]
        interest=activity["interest"]
        describe=activity["describe"]
        ability=activity["ability"]
        time=activity["time"]
        res.append([act,interest,ability,time,comment,describe])
    return res

def getUserActivity(username,act):
    info = users.find_one({"username":username})["activity"]
    for activity in info:
        if act==deword(activity["actName"]):
            interest=activity["interest"]
            ability=activity["ability"]
            time=activity["time"]
            return [word(act),interest,ability,time,username]
    return []

def getUserFriends(username):
    info = users.find_one({"username":username})["friends"]
    return info

def getActivitiesAbilityStatic(username):
    l=[]
    info = users.find_one({"username":username})["activity"]
    for activity in info:
        if activity['ability']!=0:
            l.append(True)
        else:
            l.append(False)
    return l

def getActivitiesInterestStatic(username):
    l=[]
    info = users.find_one({"username":username})["activity"]
    for activity in info:
        if activity['interest']!=0:
            l.append(True)
        else:
            l.append(False)
    return l

def getActivitiesTimeStatic(username):
    l=[]
    return l

def getCategoryAmt(category):
    #look at branches under the category and count total
    total=0
    return total

def getSubCat(category):
    category=[deword(x) for x in category]
    query=reduce(lambda s, item: s+'.'+item, category)
    l=categories.find({category[0]:{'$exists':'true'}},{query:1})
    res=[]
    for item in l:
        i=item
        for cat in category:
            i=i[cat]
        res=i
    if 'items' in res:
        return []
    return [word(x) for x in res]

def getAllCat():
    tmp=categories.find()
    l=range(10)
    for doc in tmp:
        for key in doc:
            if key != "_id":
                if key == "education":
                    l[0]=[word(x) for x in doc[key]]
                elif key == "art":
                    l[1]=[word(x) for x in doc[key]]
                elif key == "go_out":
                    l[2]=[word(x) for x in doc[key]]
                elif key == "traveling":
                    l[3]=[word(x) for x in doc[key]]
                elif key == "gambling":
                    l[4]=[word(x) for x in doc[key]]
                elif key == "games_online":
                    l[5]=[word(x) for x in doc[key]]
                elif key == "martial_arts":
                    l[6]=[word(x) for x in doc[key]]
                elif key == "services":
                    l[8]=[word(x) for x in doc[key]]
                elif key == "jobs":
                    l[9]=[word(x) for x in doc[key]]
                elif key == "sport":
                    l[7]=[word(x) for x in doc[key]]
    return l    

def hasMoreCat(category):
    category=[deword(x) for x in category]
    query=reduce(lambda s, item: s+'.'+item, category)
    l=categories.find({category[0]:{'$exists':'true'}},{query:1})
    for item in l:
        i=item
        for cat in category:
            i=i[cat]
            if 'items' in i:
                return False
    return True

def search(username,category):
    category=[deword(x) for x in category]
    query=reduce(lambda s, item: s+'.'+item, category)
    cursor=categories.find({category[0]:{'$exists':'true'}},{query:1})
    for item in cursor:
        l=recursiveCategory(item)
    s='http://maps.googleapis.com/maps/api/distancematrix/json?origins='+getUserAddress(username)+'&destinations='
    if not l:
        return l
    for user in l:
        s=s+getUserAddress(user)+'|'
    s=s+'&sensor=false'
    print 'google: ',s
    #go into resquest and sort
    googleResponse = urllib.urlopen(s)
    r = json.loads(googleResponse.read())
    pprint.pprint(r)
    indices=[]
    if r['status']=="OK":
        for el in r['rows'][0]['elements']:
            if el['status']=="OK":
                #sorting alg
                indices.append(el)
        indices=sorted(enumerate(indices), key=lambda s:s[1]['distance']['value'])
        return [getUserActivity(l[ind[0]],category[-1]) for ind in indices]
    else:
        return []

def searchByRelationship(username,category,specs=[]):
    res=search(username,category)
    if not res:
        print 'a'
    return res

def searchByAbility(item):
    res=search(username,category)
    if not res:
        print 'a'
    return res

def searchByInterest(username,category,specs=[]):
    res=search(username,category)
    if not res:
        print 'a'
    return res

def recursiveCategory(dict):
    res=[]
    if 'items' in dict:
        return dict['items']
    for index in dict:
        if index != 'more' and index != '_id':
            res=res+recursiveCategory(dict[index])
    return res

def searchByTime(item):
    res=search(username,category)
    if not res:
        print 'a'
    return res

def searchByLocation(item):
    return True

def addStandard(standard,age):
    if standard=="":
        return False
    newstandard={"standard":standard,"avrating":0,"numrating":0,"age":int(age)}
    standards.insert(newstandard);
    return True

def word(word):
    word=word.capitalize()
    if '_' in word:
        word=word.replace('_',' ')
    if '0' in word:
        word=word.replace('0','/')
    if '1' in word:
        word=word.replace('1',',')
    return word

def deword(word):
    word=word.lower()
    if ' ' in word:
        word=word.replace(' ','_')
    if '/' in word:
        word=word.replace('/','0')
    if ',' in word:
        word=word.replace(',','1')
    return word
