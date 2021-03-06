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

// Compile the template
Camera.prototype.compileTemplate = function(){
    var sources = $('#cam-template').html();
    template = Handlebars.compile(sources)
    return template(this)
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

// Append the template to the buttons
function buildButtons(){
    $('.cam-buttons').empty()
    Camera.all.forEach(function(a){
        $('.cam-buttons').append(a.compileTemplate());
    });
}

/////////////////////////////////////////////////

function Info(details) {
    this.label_sol = details.sol
    this.rover = details.rover
}


Info.prototype.compileTemplateInfo = function(){
    var source = $('#cam-details').html();
    template = Handlebars.compile(source)
    return template(this)
}


Info.all = []
Info.loadall = function(response) {
    Info.all = [];
    for (var property in response) {
        if (response[property].length > 0){
            Info.all.push(new Info(response))
        }
    }
};


function buildInfo(){
    $('.camera-info').empty();
    Info.all.forEach(function(a){
        $('.camera-info').append(a.compileTemplateInfo());
    });
}


// Event Listener to run the ajax call
$('.map-loc').on('click', function(e){
    e.preventDefault();
    rover = e.target.id;
    cap_rover = rover.charAt(0).toUpperCase() + rover.slice(1)
    // Hide from the home page
    $('#menu-home').hide();
    // Fetch the list of images with ajax call
    fetchPhotos(cap_rover);
    // Show the first navcam image (for now)
    $('#rover-view').fadeIn(600);
});


// DOES THIS WORK??????
$('.map-loc').on('click', function(e){
    e.preventDefault();
    rover = e.target.data[rover];
    cap_rover = rover.charAt(0).toUpperCase() + rover.slice(1)
    // Hide from the home page
    $('#menu-home').hide();
    // Fetch the list of images with ajax call
    fetchPhotos(cap_rover);
    // Show the first navcam image (for now)
    $('#rover-view').fadeIn(600);
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
            sol = response.sol

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

            Camera.loadall(response)
            buildButtons()

            Info.loadall(response)
            buildInfo()
            if (RoverCams.navcam){
                current_camera = RoverCams.navcam;
            }
            else {
                current_camera = RoverCams.mast;
            }
            switchMain(current_camera, count)
        }
    })
};

function switchMain(camera, count){
    $('#main-photo').attr('src', camera[count].img_src);
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

//adding the above listener to the image field.
$("#main-photo").on('click', function(){
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


// $(".mobile")


