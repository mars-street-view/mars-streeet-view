
$('article.rover-info').hide();
$('.rover-info').removeClass('hidden')
console.log($('.rover-info'));

$('.map-loc').hover(function(){
	$('article[rover-lower="' + $(this).attr('id') + '"]').fadeIn(100);
	$('.welcome').fadeOut(100);
}, function(){
	$('article.rover-info').fadeOut(100);
	$('.welcome').fadeIn(100);
})

$('.map-loc').on('click', function(){
    $('body').addClass('make-black')
})

$('.map-loc').on('click', function(){
    $('body').addClass('make-black')
    $('.nav a').addClass('nav-swap')
})

$('nav').on('click', function(e){
    e.preventDefault()
    $('body').removeClass('make-black')
    $('.nav a').removeClass('nav-swap')
    $("#rover-view").hide()
    $("#menu-home").fadeIn(1000)
})