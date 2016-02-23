var is_loading = false;
var all_post = false;
var page = 1;

$(window).scroll(function () { 
   if ($(window).scrollTop() >= $(document).height() - $(window).height() - 10) {
   		if( !is_loading && !all_post){
            loading('off');
            loadPosts();
    	}
   }
});

function loading(turn){
    // Когда посты загружены включить возможность загрузить ещё
    if(turn == 'on'){
        // $('#load_posts a').removeClass('disabled');
        $('.preloader-wrapper').hide();
        is_loading = false;
    }
    // Когда посты начали грузиться выключить возможность загрузить ещё
    else{
        // $('#load_posts a').addClass('disabled');
        $('.preloader-wrapper').show();
        is_loading = true;
    }
}

$( window ).load(function() {
    loading('off');
	loadPosts();
});

function loadPosts(){

	$.post( window.location.href, {page: page, 'profile': id_profile } )
        
		.success(function( data ) {

    		var $container = $('.feed');
			if(data == 'empty'){
				var newElems = "<h5> ¯\_(ツ)_/¯ </h5>"
			}
			else{
    			var newElems = $( data );
			}

            newElems.each(function(){
                var buildGradient = $(this).data("gradient");
                var display = $(this).find('.canvas');

                display.css('background-image', 'linear-gradient' + buildGradient);
                display.css('background-image', '-moz-linear-gradient' + buildGradient);
                display.css('background-image', '-webkit-linear-gradient' + buildGradient);
                display.css('background-image', '-o-linear-gradient' + buildGradient);
                display.css('background-image', '-ms-linear-gradient' + buildGradient);
            });


    		$container.append(newElems);

            page += 1;
            loading('on');

		}) // success || done
        
		.fail(function() {
            loading('on');
            all_post = true;
		}); // fail

} // function loadPosts
