$('#maxdistform').submit(function(e){
  $('#rangesaved').text('');
  e.preventDefault();
  var newmax = $('#max-dist').val();
  console.log(newmax);
  req = $.ajax({
    url : '/update_max',
    type : 'POST',
    data : {newmax:newmax}
  });

  req.done(function(data){
    $('#rangesaved').text('Saved!');
    })

})
