$('#messageform').on('submit', function (e) {
  e.preventDefault();
  var message = $('#send').val();
  req = $.ajax({
    url: 'sendmessage',
    type: 'POST',
    data: {
      message: message,
    }
  });

  req.done(function (data) {
    $('#send').val('')
    //$('#log').append(('<li>' + data.message + '</li>'))
  });
});



