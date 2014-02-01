$(document).ready(function(){
    $(".days").find('>input').click(function(){
	if($(this).is(':checked')){
	    $(this).parent().find('.checkbox').removeClass("hidden").find('input').prop('checked','checked');
}
	else
	    $(this).parent().find('.checkbox').addClass("hidden").find('input').prop('checked',false);
    });
    $('button[type="submit"]').click(function(){
	//json call to retreive results
    });
});
