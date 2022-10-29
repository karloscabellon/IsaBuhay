(function() {
  var video = null;
  var canvas = null;
  var photo = null;
  var startbutton = null;

  video = document.getElementById('video');
  canvas = document.getElementById('canvas');
  photo = document.getElementById('photo');
  startbutton = document.getElementById('startbutton');

  const constraints = {
    video: {
      width: {
        min: 1280,
        ideal: 1920,
        max: 2560,
      },
      height: {
        min: 720,
        ideal: 1080,
        max: 1440,
      },
    },
  }

  async function startWebcam(){
    try {
      const videoStream = await navigator.mediaDevices.getUserMedia(constraints)
      video.srcObject = videoStream;
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