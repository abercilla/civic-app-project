let geocoder;
let map;

function initialize() {
   // create map where we can geocode?
    geocoder = new google.maps.Geocoder();
    //set initial latlng at Hackbright so map is centered there
    const latlng = new google.maps.LatLng(37.7887459, -122.4115852);
    // set characteristics of map
    const mapOptions = {
        zoom: 10,
        center: latlng
    }
    //set variable to represent map
    const map = new google.maps.Map(document.getElementById("map"), mapOptions);

    

  // create marker with latlng

    // grab element from HTML page where address text is
    const address = document.getElementById("address").innerHTML;
    // pass address text through geocoder function 
    geocoder.geocode( { "address" : address}, function(results, status) {
        if (status == "OK") {
            //set the map centered around the returned latlong
            map.setCenter(results[0].geometry.location);
            //map.setZoom(18);
            // create a marker on the map where position = returned latlong
            const marker = new google.maps.Marker({
                map:map,
                position: results[0].geometry.location
            });
        } else {
            alert("Geocode was not successful for the following reason: " + status);
        }
    });
}
