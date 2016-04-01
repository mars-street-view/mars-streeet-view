$('article.rover-info').hide();
$('.rover-info').removeClass('hidden')

$('.map-loc').hover(function(){
    $('.welcome').hide();
	$('article[rover-lower="' + $(this).attr('id') + '"]').fadeIn(200);
}, function(){
	$('article.rover-info').hide();
	$('.welcome').fadeIn(200);
})
