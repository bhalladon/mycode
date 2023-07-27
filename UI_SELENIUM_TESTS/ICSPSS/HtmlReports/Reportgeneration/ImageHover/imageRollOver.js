/*
 * Image preview script 
 * Author: Siri Kumar Puttagunta
 * Date : 24/07/2013
*/
this.imagePreview = function(){	
	/* CONFIG */
		
		xOffset = 310;
		yOffset = 10;
		
		// these 2 variable determine popup's distance from the cursor
		// you might want to adjust to get the right result
		
	/* END CONFIG */
	$("a").hover(function(e){
		this.t = this.title;
		this.title = "";	
		var c = (this.t != "") ? "<br/>" + this.t : "";
		$("body").append("<p id='preview' ><img src='"+ this.href +"' alt='Image preview' style = 'width:500px; height:300px;' />"+ c +"</p>");								 
		$("#preview")
			.css("top",(e.pageY - xOffset) + "px")
			.css("left",(e.pageX + yOffset) + "px")
			.fadeIn("fast");						
    },
	function(){
		this.title = this.t;	
		$("#preview").remove();
    });	
	$("a").mousemove(function(e){
		$("#preview")
			.css("top",(e.pageY - xOffset) + "px")
			.css("left",(e.pageX + yOffset) + "px");
			
	});	
	/*$("a.preview").click(function(e){
		alert("clicked");
			
	});*/	
};


// starting the script on page load
$(document).ready(function(){
	imagePreview();
	
});