var loadFile = function(event) {
  var output = document.getElementById('output');
  var fullPath = document.getElementById('imginp').value;
  if (fullPath) {
  var startIndex = (fullPath.indexOf('\\') >= 0 ? fullPath.lastIndexOf('\\') : fullPath.lastIndexOf('/'));
  var filename = fullPath.substring(startIndex);
  if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0) {
      filename = filename.substring(1);
  }
  }

  let ext = filename.split('.')[filename.split('.').length -1];
  allowed_extensions = ['jpg', 'png', 'jpeg'];

  if (allowed_extensions.includes(ext)) {



  output.src = URL.createObjectURL(event.target.files[0]);
  output.onload = function() {
    if (this.height > this.width) {
      $('#output').attr('height', '90%');
      $('#output').attr('width', '');
    }
    else {
      $('#output').attr('height', '');
      $('#output').attr('width', '90%');
    }
    $('#newuploadtab').show();
    $('#uploadimglabel').css('position', 'absolute');
    $('#uploadimglabel').css('bottom', '-30px');
    $('#uploadimglabel').css('right', '17px');
    $('#uploadimglabel').text('Upload New');
    URL.revokeObjectURL(output.src);
   // free memor
  }
  $('#addimg').hide();
  }
  else {
    alert('The file must be an image');
  }

};
