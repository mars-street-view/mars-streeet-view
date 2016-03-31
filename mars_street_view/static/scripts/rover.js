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
var camList, cameras, cap_rover;
var rover;
var sol = 1;
var count = 0;


// // Constructor for multiple cameras
// function Camera(details) {
//     Object.keys(details).forEach(function(e, index, keys) {
//         this[e] = details[e];
//     }, this);
// }

// var template;
// // Compile the template
// Camera.prototype.compileTemplate = function(){
//     var source = $('#cam-template').html();
//     template = Handlebars.compile(source)
//     return template(this)
// }

// // var a;
// // Append the template to the buttons
// function buildButtons(){
//     Camera.all.forEach(function(a){
//         if (Object.keys(a).length > 0) {
//             console.log(a)
//             // $('.cam-buttons').append(a[0].compileTemplate());
//         }
//     });
// }


// // Fill list with objects
// Camera.all = []


// // Create the objects from the ajax call
// Camera.loadall = function(camList) {
//     new_list = camList.photos_by_cam
//     for (var property in new_list) {
//         console.log(property)
//         Camera.all.push(new Camera(new_list[property]))
//     }
// };


// Event Listener to run the ajax call
$('.map-loc').on('click', function(e){
    e.preventDefault();
    rover = e.target.id;
    cap_rover = rover.charAt(0).toUpperCase() + rover.slice(1)
    // console.log(cap_rover);
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
            // console.log(response)
            // function to make the list of cameras
            // console.log(rover);
            fullCameraList(rover, response);
            
            // Camera.loadall(camList)
            // console.log(camList)
            // buildButtons()
            // take the first image and change the 'src' attribute of the main photo (NAVCAM)
            // console.log(navcam)
            $('#main-photo').attr('src', navcam[count].img_src);
            // fetchPhotos(rover, sol);
        }
    })   
};


// Returns a list of all the objects of a rover depending on the camera
function fullCameraList(rover, camList) {
    if (rover === 'Curiosity') {
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
    // console.log(navcam)
};


// Event listener for the next image to populate main image space
$("#next-photo").on('click', function(e){
    var url = document.getElementById("main-photo").src;
    if (count < navcam.length - 1){
        newUrl = navcam[count].img_src;
        $('#main-photo').attr('src', newUrl);
        count += 1;
    } else {
        count = 0;
        sol += 1;
        console.log(rover)
        cap_rover = rover.charAt(0).toUpperCase() + rover.slice(1);
        // if sol < max_sol
        fetchPhotos(cap_rover, sol);
    }
})


// Event listener for the previous image to populate main image space
$("#prev-photo").on('click', function(e){
    var url = document.getElementById("main-photo").src;
    if (count > 0){
        newUrl = navcam[count].img_src;
        $('#main-photo').attr('src', newUrl);
        count -= 1;
    } else {
        count = 0;
        sol -= 1;
        if (sol > 0){ 
            cap_rover = rover.charAt(0).toUpperCase() + rover.slice(1);
            fetchPhotos(cap_rover, sol);
        }
    }
})


// NEXT SOL
$("#next-sol").on('click', function(e){
    cap_rover = rover.charAt(0).toUpperCase() + rover.slice(1);
    sol += 1;
    // if sol < max_sol
    fetchPhotos(cap_rover, sol);
})


// PREV SOL
$("#prev-sol").on('click', function(e){
    cap_rover = rover.charAt(0).toUpperCase() + rover.slice(1);
    sol -= 1;
    if (sol > 0){ 
        fetchPhotos(cap_rover, sol);
    }
})


