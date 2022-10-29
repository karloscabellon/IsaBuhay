(function() {
  // The width and height of the captured photo. We will set the
  // width to the value defined here, but the height will be
  // calculated based on the aspect ratio of the input stream.

  var width = 320;    // We will scale the photo width to this
  var height = 0;     // This will be computed based on the input stream

  // |streaming| indicates whether or not we're currently streaming
  // video from the camera. Obviously, we start at false.

  var streaming = false;

  // The various HTML elements we need to configure or control. These
  // will be set by the startup() function.

  var video = null;
  var canvas = null;
  var photo = null;
  var startbutton = null;

  video = document.getElementById('video');
  canvas = document.getElementById('canvas');
  photo = document.getElementById('photo');
  startbutton = document.getElementById('startbutton');

  async function startWebcam(){
    try {
      navigator.mediaDevices.getUserMedia({video: {width: {min: 1024, ideal: 1280, max:1920}, height: {min: 576, ideal: 720, max: 1080}}, audio: false});
      video.srcObject = stream;
      window.stream = stream;
    } catch (e) {
      console.log("An error occurred: " + e.toString());
      
    }
  }

  var context = canvas.getContext('2d');
  
  startbutton.addEventListener('click', () => {
    canvas.width = width;
    canvas.height = height;
    context.drawImage(video, 0, 0, width, height);
    var data = canvas.toDataURL('image/png');
    document.getElementById('webimg').value = data;
    photo.setAttribute('src', data);

  });

  
  startWebcam();
})();