// "use strict";

// RHAZ = Rear Hazard Avoidance Camera  
// FHAZ = Front Hazard Avoidance Camera
// MAST = Mast Camera
// CHEMCAM = Chemistry and Camera Complex
// MAHLI = Mars Hand Lens Imager
// MARDI = Mars Descent Imager
// NAVCAM = Navigation Camera
// PANCAM = Panoramic Camera
// MINITES = Miniature Thermal Emission Spectrometer (Mini-TES)

// Declaring the list of camera to global scope
var fhaz, rhaz, mast, chemCam, mahli, mardi, navcam, pancam, minites;

// Declaring vars in the ajax function for global use
var camList, cameras;
var rover;
var sol = 1;
var count = 0;


// // HAS NOT BEEN CREATED
// $yesterday = $('#yesterday');
// $tomorrow = $('#tomorrow');


// // Constructor for multiple cameras
// function Camera(details) {
//     Object.keys(details).forEach(function(e, index, keys) {
//         this[e] = details[e];
//     }, this);
// }


// // Compile the template
// Camera.prototype.compileTemplate = function(){
//     var source = $('#cam-template').html();
//     var template = Handlebars.compile(source)
//     return template(this)
// }

// // Fill list with objects
// Camera.all = []

// // Create the objects from the ajax call
// Camera.loadall = function(camList) {
//     camList.photos_by_cam.forEach(function(ele){
//         Camera.all.push(new Camera(ele))
//         // ele[0].url
//         // ele[0].camera_full_name
//     })
// };

// // Append the template to the buttons
// function buildButtons(){
//     Camera.all.forEach(function(a){
//         $('#cam-buttons').append(a.compileTemplate());
//     });
// }


var cap_rover;
// Event Listener to run the ajax call
$('.map-loc').on('click', function(e){
    e.preventDefault();
    rover = e.target.id;
    cap_rover = rover.charAt(0).toUpperCase() + rover.slice(1)
    console.log(cap_rover);
    // Hide from the home page 
    $('#menu-home').hide();
    // Fetch the list of images with ajax call
    fetchPhotos(cap_rover, sol);
    // Show the first navcam image (for now)
    $('#rover-view').show();
});


// Make an ajax call that will return a list
// of the photos-per-cam for a given sol and rover
// EXAMPLE: rover='Curiosity', sol=1
function fetchPhotos(rover, sol) {
    $.ajax({
        url: '/' + rover + '/' + sol,
        type: 'GET',
        dataType: 'json',
        success: function(response){            
            camList = response;
            console.log(response)
            // function to make the list of cameras
            console.log(rover);
            fullCameraList(rover, camList);
            //
            // Camera.loadall(camList)
            // take the first image and change the 'src' attribute of the main photo (NAVCAM)
            $('#main-photo').attr('src', navcam[0].img_src);
        }
    });
};


function fullCameraList(rover, camList) {
    if (rover = 'Curiosity') {
        navcam = camList.photos_by_cam[rover + '_NAVCAM'];
        fhaz = camList.photos_by_cam[rover + '_FHAZ'];
        rhaz = camList.photos_by_cam[rover + '_RHAZ'];
        mast = camList.photos_by_cam[rover + '_MAST'];
        chemCam = camList.photos_by_cam[rover + '_CHEMCAM'];
        mahli = camList.photos_by_cam[rover + '_MAHLI'];
        mardi = camList.photos_by_cam[rover + '_MARDI'];
    } else {
        navcam = camList.photos_by_cam[rover + '_NAVCAM'];
        fhaz = camList.photos_by_cam[rover + '_FHAZ'];
        rhaz = camList.photos_by_cam[rover + '_RHAZ'];
        pancam = camList.photos_by_cam[rover + '_PANCAM'];
        minites = camList.photos_by_cam[rover + '_MINITES'];
        entry = camList.photos_by_cam[rover + '_ENTRY'];
    };
    console.log(navcam)
    return navcam;
};



// Event listener for the next image to populate main image space
$("#next-photo").on('click', function(e){
    console.log("NAVCAM IN NEXT: ")
    console.log(navcam)
    var url = document.getElementById("main-photo").src;
    console.log(url)
    // var idx = navcam.indexOf();
    // console.log(idx)
    if (count < navcam.length){
        count += 1;
        newUrl = navcam[count].img_src;
        $('#main-photo').attr('src', newUrl);
    } else {
        count = 0;
        sol += 1;
        fetchPhotos(rover, sol);
    }
})


// Event listener for the previous image to populate main image space
$("#prev-photo").on('click', function(e){
    var url = document.getElementById("main-photo").src;
    var idx = navcam.indexOf(url);
    if (idx < navcam.length){
        newUrl = navcam[idx - 1].img_src;
        $('#main-photo').attr('src', newUrl);
    } else {
        sol -= 1;
        fetchPhotos(rover, sol);
    }
})



// // ????
// $spirit = $('#spirit');
// $opportunity = $('#opportunity');
// $curiosity = $('#curiosity');
// // $mainPhoto = $('#main-photo');


// Curiosity&sol=1
// http://marsstreetview.com/app?rover=
// http://marsstreetview.com/app?rover=Opportunity&sol=1
// http://marsstreetview.com/app?rover=Spirit&sol=1

