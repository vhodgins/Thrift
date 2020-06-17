$('.deletebutton').click(function(){
  let id = $(this).attr('name');
  req = $.ajax({
    url : '/delete_item',
    type: 'POST',
    data : {id:id}
  })

  req.done(function(){
    window.location.reload();
  })
})

$(document).ready(function(){
    let num = $('#followcount').text();
    if (num>999999) {
      num = String((num / 1000000).toFixed(1) + 'M')
    }
    if (num>999) {
      num = String((num / 1000).toFixed(1) + 'K');
    }
    $('#followcount').text(num);
})


$('#follow-button').click(function(){
  req = $.ajax({
    url : '/check_following',
    type: 'POST',
    data : { id : $('#follow-button').attr('store')}
  });
  req.done(function(data){
    $('#follow-button').text(data.result);
  })

})
