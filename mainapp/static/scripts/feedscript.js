var lat = 0;
var lng = 0;
function getLocation(num1,num2) {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position){

         lat = position.coords.latitude;
         lng = position.coords.longitude;

         for (let i = num1; i<=num2; i++) {
           let itemcoords = $('.location[index=' + i + ']').attr('location');
           let i_lat = itemcoords.split(',')[0];
           let i_lng = itemcoords.split(',')[1];
           let dist = getDistanceFromLatLon(lat,lng, i_lat, i_lng);
           $('.location[index=' + i + ']').text(dist+ ' Mi');

         }

    });
  }
}


function getDistanceFromLatLon(lat1,lon1,lat2,lon2) {
  var R = 6371; // Radius of the earth in km
  var dLat = deg2rad(lat2-lat1);  // deg2rad below
  var dLon = deg2rad(lon2-lon1);
  var a =
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
    Math.sin(dLon/2) * Math.sin(dLon/2)
    ;
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  var d = R * c; // Distance in km
  d = d*.62;
  d = Math.round(d);
  return d;
}

function deg2rad(deg) {
  return deg * (Math.PI/180)
}

num1 = $('.location').first().attr('index');
num2 = $('.location').last().attr('index')
getLocation(num1,num2);
