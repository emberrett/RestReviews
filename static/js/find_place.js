
function initialize() {
    var input = document.getElementById('searchTextField');
    var autocomplete = new google.maps.places.Autocomplete(input);
    google.maps.event.addListener(autocomplete, 'place_changed', function () {
        var place = autocomplete.getPlace();
        document.getElementById('latitude').value = place.geometry.location.lat();
        document.getElementById('longitude').value = place.geometry.location.lng();
        document.getElementById('rating').value = place.rating;
        document.getElementById('rest').value = place.name;
        document.getElementById('address').value = place.formatted_address;
        document.getElementById('submit-buttons').style.visibility = "visible";
    });
}
google.maps.event.addDomListener(window, 'load', initialize); 