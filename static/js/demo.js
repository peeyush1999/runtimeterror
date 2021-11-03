(function($) {

	var tabs =  $(".tabs li a");
  
	tabs.click(function() {
		var content = this.hash.replace('/','');
		tabs.removeClass("active");
		$(this).addClass("active");
    $("#content").find('p').hide();
    $("#content").find('ul').hide();
    $(content).fadeIn(200);
	});

})(jQuery);