$('article.rover-info').hide();
$('.rover-info').removeClass('hidden')

$('.map-loc').hover(function(){
    $('.welcome').hide();
	$('article[rover-lower="' + $(this).attr('id') + '"]').fadeIn(200);
}, function(){
	$('article.rover-info').hide();
	$('.welcome').fadeIn(200);
})

// $('.map-loc').on('click', function(){
//     $('body').addClass('make-black')
//     $('.nav a').addClass('nav-swap')
//     $('#logo').attr('src', "../static/MSV-WHITE.svg")
// })

// $('nav a').on('click', function(e){
//     e.preventDefault()
//     $('body').removeClass('make-black')
//     $('.nav a').removeClass('nav-swap')
//     $("#rover-view").hide()
//     $("#menu-home").fadeIn(1000)
//     $('#logo').attr('src', "../static/MSV-BLACK.svg")
// })

