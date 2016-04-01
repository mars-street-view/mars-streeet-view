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

var RoverCams = {
    fhaz: [],
    rhaz: [],
    mast: [],
    chemcam: [],
    mahli: [],
    mardi: [],
    navcam: [],
    pancam: [],
    minites: [],
    entry: []
}


// Declaring vars in the ajax function for global use
var camList, cameras, cap_rover;
var rover;
var sol = 1;
var count = 0;
var current_camera;


// Constructor for multiple cameras
function Camera(details) {
    if (details.length > 0){
        this.name = details[0].camera_full_name
        this.short_name = details[0].camera_short_name.toLowerCase()
        Object.keys(details).forEach(function(e, index, keys) {
            this[e] = details[e].img_src;
        }, this);
    }
}

// var template;
// Compile the template
Camera.prototype.compileTemplate = function(){
    var source = $('#cam-template').html();
    template = Handlebars.compile(source)
    return template(this)
}

// var a;
// Append the template to the buttons
function buildButtons(){
    $('.cam-buttons').empty()
    Camera.all.forEach(function(a){
        $('.cam-buttons').append(a.compileTemplate());
    });
}

// Fill list with objects
Camera.all = []

// Create the objects from the ajax call
Camera.loadall = function(response) {
    Camera.all = [];
    photo_list = response.photos_by_cam;
    for (var property in photo_list) {
        if (photo_list[property].length > 0){
            Camera.all.push(new Camera(photo_list[property]))
        }
    }
};


// Event Listener to run the ajax call
$('.map-loc').on('click', function(e){
    e.preventDefault();
    rover = e.target.id;
    cap_rover = rover.charAt(0).toUpperCase() + rover.slice(1)
    // console.log(cap_rover);
    // Hide from the home page
    $('#menu-home').hide();
    // Fetch the list of images with ajax call
    fetchPhotos(cap_rover);
    // Show the first navcam image (for now)
    $('#rover-view').show();
});


// Make an ajax call that will return a list
// of the photos-per-cam for a given sol and rover
// EXAMPLE: rover='Curiosity', sol=1
function fetchPhotos(rover) {
    $.ajax({
        url: '/' + rover + '/' + sol,
        type: 'GET',
        dataType: 'json',
        success: function(response){
            camList = response;
            sol = response.sol

            // console.log('res' + response.sol);
            // console.log('sol' + sol);
            console.log(response);
            if (rover === 'Curiosity') {
                RoverCams.navcam = response.photos_by_cam[rover + '_NAVCAM'];
                RoverCams.fhaz = response.photos_by_cam[rover + '_FHAZ'];
                RoverCams.rhaz = response.photos_by_cam[rover + '_RHAZ'];
                RoverCams.mast = response.photos_by_cam[rover + '_MAST'];
                RoverCams.chemcam = response.photos_by_cam[rover + '_CHEMCAM'];
                RoverCams.mahli = response.photos_by_cam[rover + '_MAHLI'];
                RoverCams.mardi = response.photos_by_cam[rover + '_MARDI'];
                RoverCams.entry = [];
                RoverCams.pancam = [];
                RoverCams.minites = [];
            } else {
                RoverCams.navcam = response.photos_by_cam[rover + '_NAVCAM'];
                RoverCams.fhaz = response.photos_by_cam[rover + '_FHAZ'];
                RoverCams.rhaz = response.photos_by_cam[rover + '_RHAZ'];
                RoverCams.pancam = response.photos_by_cam[rover + '_PANCAM'];
                RoverCams.minites = response.photos_by_cam[rover + '_MINITES'];
                RoverCams.entry = response.photos_by_cam[rover + '_ENTRY'];
                RoverCams.mast = [];
                RoverCams.chemcam = [];
                RoverCams.mahli = [];
                RoverCams.mardi = [];
            };
            // handlebar_return = []

            // or

            // for i in camList.photos_by_cam {
            //     handlebar_return.push(x[i].url)
            // }

            Camera.loadall(response)
            // console.log(camList)
            buildButtons()
            // take the first image and change the 'src' attribute of the main photo (NAVCAM)
            // console.log(navcam)
            // $('#main-photo').attr('src', navcam[count].img_src);
            current_camera = RoverCams.navcam;
            switchMain(current_camera, count)
            buildInfo(response)
            console.log(response);
            // fetchPhotos(rover, sol);
        }
    })
};

function switchMain(camera, count){
    $('#main-photo').attr('src', camera[count].img_src);
}

function Info(response) {
    this.label_sol = response.rover,
    this.rover = response.rover,
    this.cam_name = current_camera
}

function buildInfo(response){
    var source = $('#cam-details').html();
    template = Handlebars.compile(source)
    $('#camera-info').empty();
    $('#camera-info').append(template(new Info(response)))
}


// Event listener for the next image to populate main image space
$("#next-photo").on('click', function(e){
    e.preventDefault()
    var url = document.getElementById("main-photo").src;
    if (count < current_camera.length - 1){
        count += 1;
        newUrl = current_camera[count].img_src;
        switchMain(current_camera, count)
    } else {
        count = 0;
        sol += 1;
        cap_rover = rover.charAt(0).toUpperCase() + rover.slice(1);
        fetchPhotos(cap_rover);
    }
})


// $("#next-ten").on('click', function(e){
//     e.preventDefault()
//     count = 0;
//     sol += 10;
//     cap_rover = rover.charAt(0).toUpperCase() + rover.slice(1);
//     fetchPhotos(cap_rover);
// });
//
// $("#next-hundred").on('click', function(e){
//     e.preventDefault()
//     count = 0;
//     sol += 100;
//     cap_rover = rover.charAt(0).toUpperCase() + rover.slice(1);
//     fetchPhotos(cap_rover);
// });

// Event listener for the previous image to populate main image space
$("#prev-photo").on('click', function(e){
    e.preventDefault()
    var url = document.getElementById("main-photo").src;
    if (count > 0){
        count -= 1;
        newUrl = current_camera[count].img_src;
        $('#main-photo').attr('src', newUrl);
    } else {
        count = 0;
        sol -= 1;
        if (sol > 0){
            cap_rover = rover.charAt(0).toUpperCase() + rover.slice(1);
            fetchPhotos(cap_rover);
        }
    }
})


// NEXT SOL
$("#next-sol").on('click', function(e){
    e.preventDefault()
    cap_rover = rover.charAt(0).toUpperCase() + rover.slice(1);
    sol += 1;
    // if sol < max_sol
    fetchPhotos(cap_rover);
})


// PREV SOL
$("#prev-sol").on('click', function(e){
    e.preventDefault()
    cap_rover = rover.charAt(0).toUpperCase() + rover.slice(1);
    sol -= 1;
    if (sol > 0){
        fetchPhotos(cap_rover);
    }
})

$(".cam-buttons").on('click', function(e){
    camera = e.target.id
    current_camera = RoverCams[camera]
    switchMain(current_camera, 0)
})
