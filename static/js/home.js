
$(document).ready(function(){
    $("a").click(function(){
	var cat=$(this).parent().parent().prev().attr("name");
	if (cat=="cat1")
            cat='education';
        if (cat=="cat2")
            cat='art';
        if (cat=="cat3")
            cat='go_out';
        if (cat=="cat4")
            cat='travelling';
        if (cat=="cat5")
            cat='gambling';
        if (cat=="cat6")
            cat='games_online';        
        if (cat=="cat7")
            cat='martial_arts';        
        if (cat=="cat8")
            cat='sport';        
        if (cat=="cat9")
            cat='services';        
        if (cat=="cat10")
            cat='jobs';        
        if (cat=="cat11")
            cat='other';
	var sub=$(this).html();
	$.getJSON("/subcat",{category:cat,subcat:sub},function(){
	    window.location.href="/search";
	});
    });
});

