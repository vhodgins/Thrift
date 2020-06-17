$('#item-form').submit(function(e){
  if (!($('#imginp').val())) {
    e.preventDefault();
    alert('You Must Provide an Image')
  }
  for (let i=1; i<4; i++) {
      if ($('input[name=tag'+ String(i) + ']').val().match(/[^a-zA-Z0-9]/g)) {
        e.preventDefault();
        alert('Tags cannot include special characters or spaces');
        break;
      }
  }

})
