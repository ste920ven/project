from flask import request,Flask,render_template, url_for,redirect,request,session
import urllib2,json,util,requests


#for key in f.keys():
#    for value in f.getlist(key):
#        print key,":",value

app=Flask(__name__)
app.secret_key = "juN6cPlc1e"
app.config['MAX_CONTENT_LENGTH'] = 24 * 1024 * 1024 #max filesize 10mb
global ALLOWED_EXTENSIONS
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

@app.route("/",methods=["POST","GET"])
def home():
    session['category']=[]
    print 'HOME'
    if request.method=="GET":
        categories=util.getAllCat()
        if 'user' in session:
            return render_template("home.html",user=session['user'],categories=categories)
        else:
            return render_template("home.html",categories=categories)

@app.route("/sub_cat",methods=["POST","GET"])
def sub_cat():
    if request.method=="GET":
        cats=util.getSubCat(session['category'])
        if 'user' in session:
            return render_template('sub_cat.html',category=util.word(session['category'][-1]),categories=cats,user=session['user'])
        else:
             return render_template('sub_cat.html',category=util.word(session['category'][-1]),categories=cats)

            
@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="GET":
        return render_template("login.html")
    else:
        if request.form.has_key("sign_in"):
            user = str(request.form["Username"])
            password = str(request.form["Password"])
            validate = util.checkUserPass(user,password)
            print validate
            if validate == 2:
                #User doesn't exist
                return render_template("login.html",nouser=True)
            if validate == True:
                session['user'] = user
                return redirect(url_for("user",user=user))
            if validate == False:
                #Password Incorrect
                return render_template("login.html",incorrect=True)
            return render_template("login.html")
        if request.form.has_key("create_acc"):
            if 'user' in session:
                 del session['user']
            return redirect(url_for("register"))

@app.route("/user/<user>",methods=["POST","GET"])
def user(user):
    isSelf=False
    if request.method=="GET":
        noUser=False
        if 'user' in session:
            if user==session['user']:
                user=session['user']
                isSelf=True
                #ratings_list=util.getActivitiesAbilityStatic(user)
                #interests_list=util.getActivitiesInterestStatic(user)
        else:
            noUser=True
        return render_template("user.html",address=util.getUserAddress(user),birthday=util.getUserBirthday(user),email=util.getUserEmail(user),gender=util.getUserGender(user),name=util.getUserName(user),nickname=util.getUserNickname(user),phone=util.getUserPhone(user),desire=util.getUserDesire(user),activities=util.getUserActivities(user),user=user,isSelf=isSelf,noUser=noUser)
    else:
        if request.form.has_key("edit"):
            return redirect(url_for("register"))
        if request.form.has_key("save"):
            f = request.form
            data={}
            catChain=""
            for key in f.keys():
                if key == 'catChain':
                    catChain=f[key]
                elif key != 'save':
                    print 'key: ',key
                    s=key.split('_')
                    #print str(s[0])
                    if str(s[0]) not in data:
                        data[str(s[0])]={}
                    data[str(s[0])][str(s[1])]=f[key]
                    #print data
            util.updateActivities(session['user'],data,catChain)
            return render_template("user.html",address=util.getUserAddress(user),birthday=util.getUserBirthday(user),email=util.getUserEmail(user),gender=util.getUserGender(user),name=util.getUserName(user),nickname=util.getUserNickname(user),phone=util.getUserPhone(user),desire=util.getUserDesire(user),activities=util.getUserActivities(user),user=session['user'],isSelf=isSelf)
        if request.form.has_key("desire"):
            return redirect(url_for("desires"))
        if request.form.has_key("my_list"):
            return redirect(url_for("my_list"))
        if request.form.has_key("new_place"):
            return redirect(url_for("new_place"))

@app.route("/register",methods=["POST","GET"])
def register():
    if request.method=="GET":
        if 'user' in session:
            user=session['user']
            if util.getUserGender(user)=="male":
                b=True
            else:
                b=False
            return render_template("register.html",addressline=util.getUserAddressLine(user),addresscity=util.getUserAddressCity(user),addresszipcode=util.getUserAddressZip(user),birthday=util.getUserBirthDay(user),birthmonth=util.getUserBirthMonth(user),birthyear=util.getUserBirthYear(user),email=util.getUserEmail(user),firstname=util.getUserFirstName(user),lastname=util.getUserLastName(user),nickname=util.getUserNickname(user),phone=util.getUserPhone(user),user=user,gender=b)
        return render_template("register.html")
    else:
        if request.form.has_key("submit"):
            if 'user' in session:
                ###incorrect form filling debeugging
                address={'street':request.form['addressline'],'city':request.form['addresscity'],'zipcode':request.form['addresszipcode']}
                birthday=request.form['birthmonth']+''+request.form['birthday']+''+request.form['birthyear']
                name=request.form['firstname']+' '+request.form['lastname']
                util.updateUserInfo(session['user'],address,birthday,request.form['email'],request.form['gender'],name,request.form['phone'],request.form['nickname'])
                return redirect(url_for("user",user=session['user']))
            else:
                user = str(request.form["username"])
                password = str(request.form["pass1"])
                if user == "":
                    return render_template("register.html",nouser=True)
                if password == "":
                    return render_template("register.html",nopassword=True)
                elif password != str(request.form["pass2"]):
                    return render_template("register.html",notmatching=True)
                if util.addUser(user,password):
                    session['user']=user
                    return redirect(url_for("user"))
                else:
                    return render_template("register.html",taken=True)

@app.route("/standards",methods=["POST","GET"])
def standards():
    if request.method=="GET":
        if 'user' not in session:
            return render_template("standards.html")
        else:
            return render_template("standards.html",user=session['user'])
    ####
    else:
        if request.form.has_key("save"):
            print 'post'
            standard=request.form['standard-input']
            #print standard
            for key in request.form.keys():
                for value in request.form.getlist(key):
                    print key,":",value
            age=request.form['age']
            #print age
            if util.addStandard(standard,age):
                return render_template("standards.html",user=session['user'],age=age)
            else:
                return render_template("standards.html",user=session['user'],nostandard=True,age=age)

@app.route("/desires",methods=["POST","GET"])
def desires():
    if request.method=="GET":
        return render_template("desires.html",desire=util.getUserDesire(session['user']),user=session['user'])
    else:
        if request.form.has_key("save"):
            util.updateUserDesire(session['user'])
            return redirect(url_for("user"))

@app.route("/search",defaults={'field':'people'},methods=["POST","GET"])
@app.route("/search/<field>",methods=["POST","GET"])
def search(field):
    if request.method=="GET":
        category=session['category']
        user=session['user']
        if field=='people':
            #print util.searchByInterest(user,category)
            print category
            print 'res: ',util.searchByInterest(user,category)
            return render_template("people.html",category=category,user=session['user'],profiles=util.searchByInterest(user,category),categories=util.getSubCat(category),hasMoreCat=util.hasMoreCat(category))
        if field=='location':
            return render_template("location.html",category=category,user=session['user'],profiles=util.searchByLocation(category),categories=util.getSubCat(category),hasMoreCat=util.hasMoreCat(category))
        if field=='time':
            return render_template("time.html",category=category,user=session['user'],profiles=util.searchByTime(category),categories=util.getSubCat(category),hasMoreCat=util.hasMoreCat(category))

@app.route("/new_place",methods=["POST","GET"])
def new_place():
    if request.method=="GET":
        return render_template('new_place.html',user=session['user'])


@app.route("/my_list",methods=["POST","GET"])
def my_list():
    if request.method=="GET":
        user=session['user']
        #first=util.getfirst(user)...
        return render_template('my_list.html',user=session['user'])

@app.route("/logout",methods=["POST","GET"])
def logout():
    if request.method=="GET":
        if 'user' in session:
            del session['user']
        return redirect(url_for('home'))

##Ajax stuff

@app.route("/upload", methods=["GET", "POST"])
def uploadImage():
    pass

@app.route("/standard")
def showstandards():
    num=request.args['x']
    standards = util.getStandard(num)
    return json.dumps(standards)

@app.route("/addStandard")
def addStandard():
    age=request.args.get('z', '-1',type=int)
    standard=request.args.get('y','',type=str)
    print standard, age
    return json.dumps(util.addStandard(standard,age))

@app.route("/subcat")
def subcat():
    #for home
    cat=request.args.get('category')
    sub=request.args.get('subcat','')
    print 'subcat:',sub
    session['category'].append(util.word(cat))
    if sub != '':
        session['category'].append(util.word(sub))
    return json.dumps({})

@app.route("/getSubCat")
def getSubCat1():
    cat=[request.args.get('a'),request.args.get('b'),request.args.get('c'),request.args.get('d')]
    cat=removeNone(cat)
    session['tmp']=cat
    print util.getSubCat(session['tmp'])
    return json.dumps(util.getSubCat(session['tmp']))

def removeNone(l):
    res=[]
    for i in l:
        if i is not None:
            res.append(i)
    return res

if __name__=="__main__":
    app.run(debug=True)
