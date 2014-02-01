var tmpday;
var stars=0;
var category=[];
var prevCat;
var arr=['Education','Art','Go Out','Traveling','Gambling','Games Online','Martial Arts','Sport','Services','Jobs'];
var days=['s','m','t','w','r','f','a'];

$(document).ready(function(){
    fillInfo();
    $(".category").mouseenter(chooseActivity);
    $("div[name='Sun']").click(chooseTime);
    $("div[name='Mon']").click(chooseTime);
    $("div[name='Tue']").click(chooseTime);
    $("div[name='Wed']").click(chooseTime);
    $("div[name='Thu']").click(chooseTime);
    $("div[name='Fri']").click(chooseTime);
    $("div[name='Sat']").click(chooseTime);
    /*
      $(".ability-rating").find('div[type="button"]').hover(badgeTrue,badgeFalse).click(function(){
      $(this).parent().parent().prev().prev().find("input[name$='ability_info']").attr('value',$(this).text());
      });
    */
    $(".star").mouseenter(function(){
	//console.log(stars);
	var ind=$(this).attr('name');
	var ind2=ind-1;
	$(this).parent().find('i:lt('+ind+')').addClass("icon-star").removeClass("icon-star-empty");
	$(this).parent().find('i:gt('+ind2+')').addClass("icon-star-empty").removeClass("icon-star");
    }).mouseleave(function(){
	var tmp=stars;
	$(this).parent().find('i:gt('+tmp+')').addClass("icon-star-empty").removeClass("icon-star");
	$(this).parent().find('i:lt('+tmp+')').addClass("icon-star").removeClass("icon-star-empty");
    }).click(function(){
	stars=$(this).parent().find('.icon-star').length;
	$(this).parent().parent().prev().find('input[name$="interest_info"]').attr('value',stars);
    });
});

function chooseTime(){
    var tmp=$(this).attr('name');
    if(tmp=='Sun') tmpday='s';
    if(tmp=='Mon') tmpday='m';
    if(tmp=='Tue') tmpday='t';
    if(tmp=='Wed') tmpday='w';
    if(tmp=='Thu') tmpday='r';
    if(tmp=='Fri') tmpday='f';
    if(tmp=='Sat') tmpday='a';
    $(this).parent().next().empty();
    if (!$(this).hasClass('active')){
	console.log('true');
	var el = "<div class='btn' name='m'>Morning</div><div class='btn' name='a'>Afternoon</div><div class='btn' name='e'>Evening</div><div class='btn' name='n'>Night</div>"
	$(this).parent().next().append(el);
	//parse str
	/*
	for(var i=0;i<4;i++)
	    if(times[tmpday][i]){
		if(i==0)
		    $("div[name='m']").addClass('active');
		if(i==1)
		    $("div[name='a']").addClass('active');
		if(i==2)
		    $("div[name='e']").addClass('active');
		if(i==3)
		    $("div[name='n']").addClass('active');
	    }
	    */
	//
    }
    $("div[name='m']").click(updateTime0);
    $("div[name='a']").click(updateTime1);
    $("div[name='e']").click(updateTime2);
    $("div[name='n']").click(updateTime3);
}

function updateTime0(){var t=this; updateTime(t,0);}
function updateTime1(){var t=this; updateTime(t,1);}
function updateTime2(){var t=this; updateTime(t,2);}
function updateTime3(){var t=this; updateTime(t,3);}

function showBadge(t,b){
    console.log('badge');
    var i;
    if (b)
	i=$(t).text();
    else
	i=$(t).parent().find('.active').text();
    if (i==='0')
	$(t).parent().parent().find('.badge').text('Have no idea');
    else if (i==1)
	$(t).parent().parent().find('.badge').text('Just know a little bit');
    else if (i==2)
	$(t).parent().parent().find('.badge').text('Low');
    else if (i==3)
	$(t).parent().parent().find('.badge').text('Moderate');
    else if (i==4)
	$(t).parent().parent().find('.badge').text('Good');
    else if (i==5)
	$(t).parent().parent().find('.badge').text('Competitive, can play/do well');
    else if (i==6)
	$(t).parent().parent().find('.badge').text('Top of school/town');
    else if (i==7)
	$(t).parent().parent().find('.badge').text('Top of small, medium city');
    else if (i==8)
	$(t).parent().parent().find('.badge').text('Top of big city/state/county');
    else if (i==9)
	$(t).parent().parent().find('.badge').text('Top of country/continent');
    else if (i==10)
	$(t).parent().parent().find('.badge').text('Top of the world');
    else $(t).parent().parent().find('.badge').text('');
}

function badgeTrue(){var t=this; showBadge(t,true);}
function badgeFalse(){var t=this; showBadge(t,false);}

function addActivity(){
    var cat=$(this).html();
    var el='<div class="activity_wrapper span12"><div class="row"><legend></legend><h4 class="p1">'+cat+'</h4><div class="info"><input type="hidden" name="catChain" value="'+category.join()+'"><input type="hidden" name="'+cat+'_category" value="'+category[0]+'"><input type="hidden" name="'+cat+'_interest_info" value=""><input type="hidden" name="'+cat+'_ability_info" value=""><input type="hidden" name="'+cat+'_times_info" value=""><input type="hidden" name="'+cat+'_static_info" value="False"></div><div class="span12"><h5>Interest</h5><div class="ratings-container"><i class="star icon-star-empty" name="1"></i><i class="star icon-star-empty" name="2"></i><i class="star icon-star-empty" name="3"></i><i class="star icon-star-empty" name="4"></i><i class="star icon-star-empty" name="5"></i></div></div><div class="span12 ability-rating"><h5>Ability</h5><div class="btn-group" data-toggle="buttons-radio"><button type="button" class="btn" >0</button><button type="button" class="btn" >1</button><button type="button" class="btn" >2</button><button type="button" class="btn" >3</button><button type="button" class="btn" >4</button><button type="button" class="btn" >5</button><button type="button" class="btn" >6</button><button type="button" class="btn" >7</button><button type="button" class="btn" >8</button><button type="button" class="btn" >9</button><button type="button" class="btn" >10</button></div><span class="badge"></span></div><div class="span7"><h5>Self Describe</h5><input type="text" name="'+cat+'_describe" value=""><h6>Times Available</h6><div class="btn-group" data-toggle="buttons-checkbox"><div class="btn" name="Sun">Sun</div><div class="btn" name="Mon">Mon</div><div class="btn" name="Tue">Tues</div><div class="btn" name="Wed">Weds</div><div class="btn" name="Thu">Thurs</div><div class="btn" name="Fri">Fri</div><div class="btn" name="Sat">Sat</div></div><div class="btn-group times" data-toggle="buttons-checkbox"></div></div>';
    console.log($(this).html());
    var tis=$("a[name='addActivity']");
    var tmp=$('#activities')
    $(tis).parent().parent().prepend(el).prepend(tmp);
    $(tis).next().remove();
    $(tis).remove();
    //add js functionality to new activity
    $(".star").mouseenter(function(){
	//console.log(stars);
	var ind=$(this).attr('name');
	var ind2=ind-1;
	$(this).parent().find('i:lt('+ind+')').addClass("icon-star").removeClass("icon-star-empty");
	$(this).parent().find('i:gt('+ind2+')').addClass("icon-star-empty").removeClass("icon-star");
    }).mouseleave(function(){
	var tmp=stars;
	$(this).parent().find('i:gt('+tmp+')').addClass("icon-star-empty").removeClass("icon-star");
	$(this).parent().find('i:lt('+tmp+')').addClass("icon-star").removeClass("icon-star-empty");
    }).click(function(){
	stars=$(this).parent().find('.icon-star').length;
	console.log(stars);
	$(this).parent().parent().prev().find('input[name$="interest_info"]').attr('value',stars);
    });
    $("div[name='Sun']").click(chooseTime);
    $("div[name='Mon']").click(chooseTime);
    $("div[name='Tue']").click(chooseTime);
    $("div[name='Wed']").click(chooseTime);
    $("div[name='Thu']").click(chooseTime);
    $("div[name='Fri']").click(chooseTime);
    $("div[name='Sat']").click(chooseTime);
    $(".ability-rating").find('button[type="button"]').hover(badgeTrue,badgeFalse).click(function(){
	$(this).parent().parent().prev().prev().find("input[name$='ability_info']").attr('value',$(this).text());
    });
    return
}

function updateTime(t,i){
    var timeNode=$(t).parent().parent().parent().children('.info').children('[name$="_times_info"]');
    var time=timeNode.attr('value');
    //times[tmpday][i]=!times[tmpday][i];
    if(time.indexOf(tmpday+i)>-1)
	time=time.replace(tmpday+i,'');
    else
	time=time.replace('',tmpday+i); 
    timeNode.attr('value',time);
}

function addExchange(){

}

function chooseActivity(){
    if(prevCat == null){
    }else if(arr.indexOf($(this).html())>-1){
	category=[];
    }else if ($.contains(this.parentNode,prevCat)||prevCat==this){
	category.pop();
	category.pop();
    }else if ($.contains(prevCat,this.parentNode)){
    }else if ($.contains(this.parentNode.parentNode,prevCat.parentNode)){
	category.pop();
	category.pop();
    }
    else{category.pop();}
    category.push($(this).html());
    prevCat=this.parentNode;
    var target=$(this).parent();
    console.log(category);
    target.children('ul').remove();
    if (category.length==1)
	$.getJSON("/getSubCat",{a:category[0]},function(data){
	    if (data.length>0){
		//create el
		var el='<ul class="dropdown-menu">';
		for (var i=0;i<data.length;i++){
		    el=el+'<li class="dropdown-submenu"><a>'+data[i]+'</a></li>';
		}
		el=el+'</ul>';
		target.append(el);
		target.children('ul').children('li').children('a').mouseenter(chooseActivity);
	    }else{
		target.removeClass('dropdown-submenu');
		target.children('a').click(addActivity);
	    }
	});
    else if (category.length==2)
	$.getJSON("/getSubCat",{a:category[0],b:category[1]},function(data){
	    if (data.length>0){
		//create el
		var el='<ul class="dropdown-menu">';
		for (var i=0;i<data.length;i++){
		    el=el+'<li class="dropdown-submenu"><a>'+data[i]+'</a></li>';
		}
		el=el+'</ul>';
		target.append(el);
		target.children('ul').children('li').children('a').mouseenter(chooseActivity);
	    }else{
		target.removeClass('dropdown-submenu');
		target.children('a').click(addActivity);
	    }
	});
    else if (category.length==3)
	$.getJSON("/getSubCat",{a:category[0],b:category[1],c:category[2]},function(data){
	    if (data.length>0){
		//create el
		var el='<ul class="dropdown-menu">';
		for (var i=0;i<data.length;i++){
		    el=el+'<li class="dropdown-submenu"><a>'+data[i]+'</a></li>';
		}
		el=el+'</ul>';
		target.append(el);
		target.children('ul').children('li').children('a').mouseenter(chooseActivity);
	    }else{
		target.removeClass('dropdown-submenu');
		target.children('a').click(addActivity);
	    }
	});
    else if (category.length==4)
	$.getJSON("/getSubCat",{a:category[0],b:category[1],c:category[2],d:category[3]},function(data){
	    if (data.length>0){
		//create el
		var el='<ul class="dropdown-menu">';
		for (var i=0;i<data.length;i++){
		    el=el+'<li class="dropdown-submenu"><a>'+data[i]+'</a></li>';
		}
		el=el+'</ul>';
		target.append(el);
		target.children('ul').children('li').children('a').mouseenter(chooseActivity);
	    }else{
		target.removeClass('dropdown-submenu');
		target.children('a').click(addActivity);
	    }
	});
    console.log(category);
}

function fillInfo(){
    iL=$('.info').find("input[name$='interest_info']").parent().next();
    for(var i=0;i<iL.length;i++){
	var interest=parseInt($(iL[i]).prev().find("input[name$='interest_info']").attr('value'));
	$(iL[i]).find('i:lt('+interest+')').addClass("icon-star").removeClass("icon-star-empty");	
    }
    aL=$('.info').find("input[name$='ability_info']").parent().next().next();
    for(var i=0;i<aL.length;i++){
	var ability=parseInt($(aL[i]).prev().prev().find("input[name$='ability_info']").attr('value'));
	var buttons=$(aL[i]).find('button.btn');
	$(buttons.get(ability)).addClass('active').prop('disabled',false);	
    }
    var tL=$('.info').find("input[name$='times_info']").parent().next().next().next();
    console.log(tL);
    for(var i=0;i<tL.length;i++){
	var time=$(tL[i]).prev().prev().prev().find("input[name$='times_info']").attr('value');
	for (var k=0;k<days.length;k++){
	    if (time.indexOf(days[k]+'0')!=-1)
		$(tL[i]).find('div.btn');
	}
    }
}



