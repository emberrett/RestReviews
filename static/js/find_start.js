const startLongParam = (new URL(document.location)).searchParams.get("startLong");
function initialize() {
    var input = document.getElementById('searchTextField');
    var autocomplete = new google.maps.places.Autocomplete(input);
    google.maps.event.addListener(autocomplete, 'place_changed', function () {
        var place = autocomplete.getPlace();
        var lat = parseFloat(place.geometry.location.lat()).toFixed(6);
        var long = parseFloat(place.geometry.location.long()).toFixed(6);
        let url = new URL(window.location.href);



        url.searchParams.set('startLat', lat);
        url.searchParams.set('startLong', long);
        window.location.assign(url);
    });
}
google.maps.event.addDomListener(window, 'load', initialize); 