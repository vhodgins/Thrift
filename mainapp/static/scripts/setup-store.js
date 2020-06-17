var data = [];
var url_exists='';

$('#submit').click(function(){
  let tags =[];
  $(".tags").each(function() {
  tags.push($(this).val());
});
  tags = tags.join(' ');
  let address = $('#Address').val();
  let city = $('#City').val();
  let state = $('#State').val();
  let zip = $('#Zip').val();
  address = [address, city, state, zip].join(' ');

  req = $.ajax({
    url : '/submit_store',
    type : 'POST',
    data :
    {
      name : data[0],
      address : address,
      url : $('#URL').val(),
      description : data[3],
      tags : tags
    }
  });
  req.done(function(data){
    if (data.result=='success'){
      $('#loading-panel').hide(100);
      $('#done').show(100);
      $('#reload-page').focus();
    }
  })
})

$('#reload-page').click(function(){
  window.location.reload();
})


$('.lastfield').keyup(function(){
  if ($(this).val()) {
    n = $(this).attr('num');
    $('.next[num=' + n + ']').fadeIn(150);
  } else {
    $('.next[num=' + n + ']').fadeOut(150);
  }
})


$(document).ready(function() {
  $('#Okaybtn').focus();
});


$('.next').click(function() {
  let num = $(this).attr('num');

  if (num!='4') {
  $('[number=' + num + ']').hide();
  $('[number=' + String(parseInt(num) + 1) + ']').show(150);
  $('.pagecontent').focus();
  $('.typing').focus();
  data[num - 2] = $('.pagecontent[num=' + num + ']').val();
}
  if (num=='4') {

    req = $.ajax({
      url: '/url_exists',
      method: 'POST',
      data: {
        name:  $('.pagecontent[num=4]').val()
      }
    });
    req.done(function(data) {
      url_exists = data.result;
      if (url_exists=='true') {
        alert('Unfortunately, this Url is already in use.');
      }
      else {
        $('[number=' + num + ']').hide();
        $('[number=' + String(parseInt(num) + 1) + ']').show(150);
        $('.pagecontent').focus();
        data[num - 2] = $('.pagecontent[num=' + num + ']').val();
      }
    });


  }
  if (num == 2) {
    req = $.ajax({
      url: '/check_url',
      method: 'POST',
      data: {
        name: data[0]
      }
    });
    req.done(function(data) {
      $('#URL').attr('value', data.url);
    });
  }
  $('.lastfield').focus();
});

$('.pagecontent').keypress(function(e) {
  if ((e.which == 13) && ($(this).val())) {
    let num = $(this).attr('num');

    if (num!='4') {
    $('[number=' + num + ']').hide();
    $('[number=' + String(parseInt(num) + 1) + ']').show(150);
    $('.pagecontent').focus();
    $('#Address').focus();
    data[num - 2] = $('.pagecontent[num=' + num + ']').val();
  }
    if (num=='4') {

      req = $.ajax({
        url: '/url_exists',
        method: 'POST',
        data: {
          name:  $('.pagecontent[num=4]').val()
        }
      });
      req.done(function(data) {
        url_exists = data.result;
        if (url_exists=='true') {
          alert('Unfortunately, this Url is already in use.');
        }
        else {
          $('[number=' + num + ']').hide();
          $('[number=' + String(parseInt(num) + 1) + ']').show(150);
          $('.pagecontent').focus();
          data[num - 2] = $('.pagecontent[num=' + num + ']').val();
        }
      });


    }
    if (num == 2) {
      req = $.ajax({
        url: '/check_url',
        method: 'POST',
        data: {
          name: data[0]
        }
      });
      req.done(function(data) {
        $('#URL').attr('value', data.url);
      });
    }
    $('.lastfield').focus();
  }
});


$('.back').click(function() {
  let num = $(this).attr('num');
  $('[number=' + num + ']').hide();
  $('[number=' + String(parseInt(num) - 1) + ']').show(150);
  $('.pagecontent').focus();
  $('.next[num=' + String(parseInt(num)-1) + ']').show()
});

$('.pagecontent').keyup(function() {
  if ($(this).val()) {
    n = $(this).attr('num');
    $('.next[num=' + n + ']').fadeIn(150);
  } else {
    $('.next[num=' + n + ']').fadeOut(150);
  }
});
