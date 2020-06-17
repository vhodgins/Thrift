$('#register').submit(function(e) {
  let b = $(this).find('input[name="type"]:checked').val();
  var lat = 0;
  var lng = 0;
    e.preventDefault();
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position){

           lat = position.coords.latitude;
           lng = position.coords.longitude;
           loc = String(lat) + ',' + String(lng);
           e.preventDefault();
           req = $.ajax({
             url: 'register_account',
             type: 'POST',
             data: {
               email   : $('#register').find('input[name="email"]').val(),
               username: $('#register').find('input[name="name"]').val(),
               password: $('#register').find('input[name="password"]').val(),
               business: $('#register').find('input[name="type"]:checked').val(),
               loc     : loc,
               remember: $('#register').find('input[name="remember"]').prop('checked')
             }
           });

           req.done(function(data) {
             if (data.failure) {
               alert('Sorry, the ' + data.failure + ' you chose is already taken.')
             }
             else {
               if (b=='true'){
                 window.location.href = document.location.href + 'store';
               }
               if (b=='false') {
                 window.location.reload();
               }

             }
           });

      });
    }



});

$('#login').submit(function(e) {
  e.preventDefault();
  req = $.ajax({
    url: 'login',
    type: 'POST',
    data: {
      username: $(this).find('input[name="name"]').val(),
      password: $(this).find('input[name="password"]').val(),
      remember: $(this).find('input[name="remember"]').prop('checked')
    }
  });

  req.done(function(data) {
    if (data.failure) {
      alert('Sorry, your username or password is incorrect.')
    }
    else {

      window.location = document.location.href + '/store';
    }
  })

});

$('#shift-to-register').click(function(){
  $('#login').hide();
  $('#register').show(150);
});

$('#shift-to-login').click(function(){
  $('#register').hide();
  $('#login').show(150);
});
