
$yesterday = $('#yesterday');
$tomorrow = $('#tomorrow');
$next = $('#next');
$prev = $('#prev');
$spirit = $('#spirit');
$opportunity = $('#opportunity');
$curiosity = $('#curiosity');
$homeMenu = $('#menu-home');
$roverView = $('#rover-view');
$location = $('.map-loc');
$mainPhoto = $('#main-photo');
var photoList;
var rover;
var sol = 1;

function photoSwapper(jqobj, url){
    jqobj.attr('src', url);
}


function getMorePictures(rover, sol, target){
    $.ajax({
        url: '/' + rover + '/' + sol,
        type: 'GET',
        dataType: 'json',
        success: function(response){
            console.log(response);
            photoList = response;
            console.log(photoList[0].url);
            $mainPhoto.attr('src', photoList[0].url);
            // photoSwapper(target, photoList[0].url);
        }
    });
}

$mainPhoto.on('click', function(e){
    url = e.target.src;
    idx = photoList.indexOf(url);
    if (idx < photoList.length){
        newUrl = photoList[idx + 1].url;
        $mainPhoto.attr('src', newUrl);
    } else {
        sol += 1;
        getMorePictures(rover, sol, e.target);
    }
});

$location.on('click', function(e){
    e.preventDefault();
    rover = e.target.id;
    console.log(rover);
    console.log(sol);
    rover[0] = rover[0].toUpperCase();
    console.log(rover);
    photoList = [];

    //hide stuff
    $homeMenu.hide();
    //make ajax call
    getMorePictures(rover, sol, e.target);
    //show stuff
    $roverView.show();
});


// Curiosity&sol=1
// http://marsstreetview.com/app?rover=
// http://marsstreetview.com/app?rover=Opportunity&sol=1
// http://marsstreetview.com/app?rover=Spirit&sol=1

