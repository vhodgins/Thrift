
  var noneleft = false;

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



  function isScrolledIntoView(elem)
  {
      var docViewTop = $(window).scrollTop();
      var docViewBottom = docViewTop + $(window).height();

      var elemTop = $(elem).offset().top;
      var elemBottom = elemTop + $(elem).height();

      return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
  }


    function onScrollLoad(){
    try {
    if (isScrolledIntoView($('#last'))) {
    last_item = $('#lastitem').attr('last');
    $('#lastitem').attr('id', '');
    req = $.ajax({
      url: '/fetch_more_items',
      type: 'POST',
      data: {number : last_item}
    });

    req.done(function(data){
      
      $('#last').hide();
      $('#last').attr('id', '');


      let length = Object.keys(data).length -3;
      var user_location = data[11];
      let lat = user_location.split(',')[0]
      let lng = user_location.split(',')[1]
      var new_last = data[12];

      for (let i=0; i<length; i++){

        try {
        var content = data[i].split('<');
        let IMG_HEIGHT = content[4]
        let DESCRIPTION = content[0];
        let LOCATION = content[2];
        let ilat = LOCATION.split(',')[0]
        let ilng = LOCATION.split(',')[1]
        let DISTANCE = getDistanceFromLatLon(lat,lng,ilat,ilng);
        let IMG = content[3];
        let MAPS_LINK = user_location + '/' + LOCATION;
        let STORE = String(content[1]);
        let CLICKTHROUGH = ''
        if (data[13]) {
        CLICKTHROUGH = 'clickthrough';
        }



        a =    `<div class='card ' id='feedcontent' style='margin:auto; margin-bottom:20px; width:600px; '>
        <h4 class='mt-2' id='post-heading' style='margin-left:20px; font-weight:200;'>`+DESCRIPTION+`</h4>
          <h5 class='mt-2' id='post-heading-mobile' style='margin-left:20px; font-weight:200;'>`+DESCRIPTION+`</h5>
          <span class='location' style='position:absolute; right:20px; top:14px; font-weight:400; font-size:12pt;'  >`+DISTANCE+` Mi</span>
          <div class='' style=' background-color: rgba(210, 210, 210, 0.61); width:100%; margin-left:-1px; margin-top:10px;'>
            <hr style='margin-bottom:-10px; margin-top:-1px;'>
            <img src='/static/items/` + IMG + `' alt=''  width='80%'  height='`+ IMG_HEIGHT + `' style='display: block; margin:auto  ; margin-top:10px; margin-bottom:10px; '>
            <hr style='margin-top:-10px; margin-bottom:-1px;'>
          </div>
          <a href='http://localhost:5000/store_redirect/` + STORE +`' style='margin-bottom:15px; margin-left:20px; margin-top:15px'  class='text-primary'>See item in store</a>
          <a href='https://www.google.com/maps/dir/` + MAPS_LINK + `'  target='_blank' style='position:absolute; right:20px; bottom:10px;' class='btn btn-success btn-sm  `+ CLICKTHROUGH +`'>Find Store</a>
        </div>`;



        if (i==length-1){

          a = a + `<div id="last">

          <div class="card" style=" width:600px; margin:auto;">
            <p style="text-align:center; margin-top:20px;" last="`+ new_last + `" id="lastitem">Loading More Items</p>
            <div class="spinner-border text-primary m-auto"  role="status">
        <span class="sr-only">Loading...</span>
        </div>
        <div style="height:20px;"></div>

          </div>
          <div style="height:100px;"></div>
        </div>`
      }

      $('.content').append(a);


      }
      catch(err) {
        console.log('Error 1');
      }
      }
    })
  }
}

  catch(err) {
    if (!noneleft){
    noneleft = true;
    let a = `  <div class="card" style=" width:600px; margin:auto;">
        <p style="text-align:center; margin-top:20px;" >Couldn't find more items, sorry!</p>

    <div style="height:20px;"></div>

      </div>
      <div style="height:100px;"></div>`
    $('.content').append(a);
  }
}
}

window.onscroll = onScrollLoad;
