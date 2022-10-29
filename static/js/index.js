(function() {
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