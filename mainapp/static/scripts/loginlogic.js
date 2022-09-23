$('#register').submit(function(e) {
  let b = $(this).find('input[name="type"]:checked').val();

    e.preventDefault();

           e.preventDefault();
           req = $.ajax({
             url: 'register_account',
             type: 'POST',
             data: {
               username: $('#register').find('input[name="name"]').val(),
               password: $('#register').find('input[name="password"]').val(),
               charactertype: $('#register').find('input[name="type"]:checked').val(),
               partycode: $('#register').find('input[name="partycode"]').val(),
               remember: $('#register').find('input[name="remember"]').prop('checked')
             }
           });

           req.done(function(data) {
             if (data.failure) {
               alert('Sorry, the ' + data.failure + ' you chose is already taken.')
             }
             else {
               if (b=='true'){
                 window.location.href = document.location.href + 'game';
               }
               if (b=='false') {
                 window.location.reload();
               }

             }
           });
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
      window.location = document.location.href + 'game';
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
