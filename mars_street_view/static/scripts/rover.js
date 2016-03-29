
yesterday = $('#yesterday');
tomorrow = $('#tomorrow');
next = $('#next');
prev = $('#prev');

yeserday.addEventListener();

function getMorePictures(rover, sol){
    $.ajax({
        url: '/' + rover + '/' + sol,
        type: 'GET',
        dataType: 'json',
        success: function(response){
            return json.parse(response);
        }
    });
}



