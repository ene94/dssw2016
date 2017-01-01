var map;
function initMap() {
  //get Geo Info
  var latitud = document.getElementById('lat').innerHTML;
  var longitud = document.getElementById('lng').innerHTML;
  var address = document.getElementById('address').innerHTML;
  var myLatLng = new google.maps.LatLng(parseFloat(latitud),parseFloat(longitud));
  //draw Map
  map = new google.maps.Map(document.getElementById('map'), {
    center: myLatLng,
    zoom: 10
  });
  //point marker
  var marker = new google.maps.Marker(
    {
      position: myLatLng,
      map: map,
      title: address
    }
  );
}
