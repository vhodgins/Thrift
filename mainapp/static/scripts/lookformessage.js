var intervalID = window.setInterval(function() {
    
    console.log("Polling...")
    req = $.ajax({
      url: 'lookformessages',
      type: 'GET'
    });
  
    req.done(function (data) {
        console.log(data.messages[0]);
        $('#log').html('');
        for (let i=data.messages.length-1; i>=0; i--){
            $('#log').append("<li>"+data.messages[i]+"</li>");
        }
    });


}, 1000);