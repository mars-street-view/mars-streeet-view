
$('article.rover-info').hide();
$('.rover-info').removeClass('hidden')

$('.map-loc').hover(function(){
	$('article[rover="' + $(this).attr('id') + '"]').fadeIn(100);
	$('.welcome').fadeOut(100);
}, function(){
	$('article.rover-info').fadeOut(100);
	$('.welcome').fadeIn(100);
})
