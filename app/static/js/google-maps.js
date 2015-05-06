var map = null;    
var regionArray = []; 
var markers = [];
var sensorArray = [];
var infowindow = null;
var sensorJSONRaw = {};

function initialize() {
  var mapOptions = {
    center: { lat: 40.036137, lng: -75.340919},
      zoom: 17,
      scrollwheel: false
  };

  map = new google.maps.Map(document.getElementById('map-canvas'),
    mapOptions);

    google.maps.event.addListener(map, 'click', function(event) {
    addMarker(event.latLng);
  });


   /* initialise the infowindows */
  infowindow = new google.maps.InfoWindow({
    content: "Waiting for content..."
  });
}

function showSensors() {

  //cannot make global due to asynchronous Ajax Calls
  var callResult = {};

  $.ajax({url:"http://127.0.0.1:5000/findSensors",success:function(result) { //change url
    callResult = result;
    sensorJSONRaw = callResult;

    for (x in callResult) {

      var coordinate = new google.maps.LatLng(callResult[x].location.latitude, callResult[x].location.longitude);
      sensorArray.push(coordinate);

      //window.alert(callResult[x].location.latitude);

      var marker = new google.maps.Marker({
        position: coordinate,
        map: map,
        //animation: google.maps.Animation.DROP,
        title: callResult[x].name
      });

//      google.maps.event.addListener(marker, 'click', toggleBounce);

      markers.push(marker);
      marker.setMap(map);


       bindInfoWindow(marker, map, infowindow, callResult[x]._id);
    } 


    for (var i = 0; i < markers.length; i++) {
      var m = markers[i];
      google.maps.event.addListener(m, 'click', function () {
        //infowindow.setContent(this.html);  //-->this.html references the information that I want to put in the dialog boxes
        infowindow.open(map, this);
      });
    }



  /*******TODO 
      -Make this more robust and create markers based on Database and names... might need another AJAX call.
      -Also allow for marker array to be checked first for cached markers to be added before performing AJAX call.
  ********/

}}); 

}

function bindInfoWindow(marker, map, infowindow, id) {
    google.maps.event.addListener(marker, 'click', function() {
        infowindow.setContent(getInfoContent(id));
        infowindow.open(map, marker);
        updateWindowPane(id);
    });
}

function createMarkers(type) {
  //modify the views to handle different types of points
}

function getInfoContent(id) {
    var content;
    $.ajax({async: false, url: "http://127.0.0.1:5000/getInfoPane/" + id, success:function(result) { //change url
        content = result;
    }});

  return content;
}

function hideMarkers() {
  for(x in markers) {
    markers[x].setMap(null);  
    //markers[x].remove();
  }
}

function toggleBounce() {

  if (marker.getAnimation() != null) {
    marker.setAnimation(null);
  } else {
    marker.setAnimation(google.maps.Animation.BOUNCE);
  }
}

function updateWindowPane(id) {
      $.ajax({async: false, url: "http://127.0.0.1:5000/updateWindowPane/" + id, success:function(result) { //change url
        
        $( ".info" ).replaceWith($(result));
    }});
}

google.maps.event.addDomListener(window, 'load', initialize);