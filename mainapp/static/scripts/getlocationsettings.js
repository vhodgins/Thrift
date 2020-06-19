
var x = document.getElementById("demo");
var lat = '';
var lng = '';
function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function showPosition(position) {
   lat = position.coords.latitude;
   lng = position.coords.longitude;
   req = $.ajax({
     url : '/get_loc',
     type : 'POST',
     data : {lat:lat , lng:lng}
   })

   req.done(function(data){
     let location = data.location;
     $('#loc').text(location);
   })

}

getLocation();
