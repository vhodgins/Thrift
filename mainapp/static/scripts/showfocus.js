$('.typing').keyup(function(e){
  if (($('#Address').val() && $('#City').val()) && $('#State').val()) {

    if (e.which == 13) {
      $('[number=3]').hide();
      $('[number=4]').show(150);
      $('.pagecontent').focus();

    }

    $('#nextbuttonaddress').show();
  }
  else {
    $('#nextbuttonaddress').hide();
  }
})
