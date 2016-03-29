$('article.rover-info').hide();
$('.rover-info').removeClass('hidden')

$('.map-loc').hover(function(){
	$('article[rover="' + $(this).attr('id') + '"]').fadeIn();
	$('.welcome').fadeOut();
}, function(){
	$('article.rover-info').fadeOut();
	$('.welcome').fadeIn();
})
