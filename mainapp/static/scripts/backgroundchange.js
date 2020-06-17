$('#backimg').change(function(){
  $('#backgroundForm').submit();
})

$('#backgroundForm').submit(function(){
  let name = $('#backimg').val()
  let extensions = ['jpg', 'png', 'jpg'];
  if (!(extensions.includes(name.split('.')[name.split('.').length -1]))) {
    alert('File must be an image.');
    e.preventDefaut();
  }
});


$('a[name="change-background"]').click(function(){
  $('#change-background').slideDown(100);
});

$('#close-change-background').click(function(){
  $('#change-background').slideUp(150);
})
