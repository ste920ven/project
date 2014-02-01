$(document).ready(function(){
 $.ajaxSetup({
        async: false
    });
    if($('#num').attr('value')){
	showStandards($('#num').attr('value'));
    }
    if($('p.error').length>0){
	addStandard();
    }
});


function showStandards(num){
    //clear current standards
    $("#standards_list").empty();
    $.getJSON("/standard",{x:num},function(data){
	for (var i=0;i<data.length;i++){
	    var el='<p>'+data[i]+'</p>';
	    $("#standards_list").append(el);
	}
	var b = "<button class='btn' name='add' role='button' onclick=addStandard()>Add</button>";
	$("#standards_list").append(b);
    });
    $("#num").attr('value',num);
    return;
}

function addStandard(){
    $("button[name='add']").remove();
    var t = "<input type='text' name='standard-input'><br>"
    $("#standards_list").append(t);
    var n = $("#num").attr("value");
    var b = "<button class='btn' name='save'>Save</button>";
    $("#standards_list").append(b);
    /*
    $('div.btn').click(function(){
	$("p.error").remove();
	var info = $("input[name='standard-input']").attr('value');
	console.log(info);
	$.getJSON("/addStandard",{z:n,y:info},function(data){
	    console.log('data: '+data+'.');
	    if(data){
		showStandards(n);
	    }
	    else{
		var el='<p class="error">Please enter a standard</p>'
		$('#standards_list').append(el);
	    }
	});
    });
*/
}
