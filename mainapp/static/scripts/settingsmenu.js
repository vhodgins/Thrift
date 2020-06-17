$('.s-link-a').click(function(){
  $(this).blur();
  let type = $(this).attr('type');
  $('.setting-data').hide();
  $('#' + type).fadeIn(150);
})
