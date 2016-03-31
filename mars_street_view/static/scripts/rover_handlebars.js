
// // $(windows).load(function)

// (function(module){

//     // var Camera = {}

//     // Constructor for multiple cameras
//     function Camera(details) {
//         Object.keys(details).forEach(function(e, index, keys) {
//             this[e] = details[e];
//         }, this);
//     }
// <!-- {{#Camera[0]}} -->
//         <img src="{{img_src}}">
//         <!-- <img src=""> -->
//         <h5>{{camera_short_name}}<h5>
//       <!-- {{/Camera[0]}} -->

//     Camera.all = []

//     // Compile the template
//     Camera.prototype.compileTemplate = function(){
//         var source = $('#cam-template').html();
//         var template = Handlebars.compile(source)
//         return template(this)
//     }

//     // Fill list with objects

//     // Create the objects from the ajax call
//     Camera.loadall = function(camList) {
//         camList.photos_by_cam.forEach(function(ele){
//             Camera.all.push(new Camera(ele))
//         })
//     };

//     // Append the template to the buttons
//     function buildButtons(){
//         Camera.all.forEach(function(a){
//             $('#cam-buttons').append(a.compileTemplate());
//         });
//     }

//     module.Camera = Camera;

// })(window);