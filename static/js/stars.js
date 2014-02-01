var stars=0;

$(document).ready(function(){
    $(".star").mouseenter(function(){
	//console.log(stars);
	var ind=$(this).attr('name');
	var ind2=ind-1;
	console.log(ind);
	$(this).parent().find('i:lt('+ind+')').addClass("icon-star").removeClass("icon-star-empty");
	$(this).parent().find('i:gt('+ind2+')').addClass("icon-star-empty").removeClass("icon-star");
    }).mouseleave(function(){
	var tmp=stars;
	$(this).parent().find('i:gt('+tmp+')').addClass("icon-star-empty").removeClass("icon-star");
	$(this).parent().find('i:lt('+tmp+')').addClass("icon-star").removeClass("icon-star-empty");
    }).click(function(){
	stars=$(this).parent().find('.icon-star').length;
	
    })
});
