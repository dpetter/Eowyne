$(document).ready(function(){
	
	
    	$("#infofield").delay( 3000 ).slideUp("slow");

    	
	








})


function ajax_popup(container, url) {
	$.get(url, function(data) {
		$(container).html(data);
		$(container).popup("show");
	});
}
