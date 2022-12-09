var startLong = (new URL(document.location)).searchParams.get("startLong");
var startLat = (new URL(document.location)).searchParams.get("startLat");

function calcCrow(elementID, endLat, endLong) {

    let R = 6371; // km
    let dLat = toRad(endLat - startLat);
    let dLon = toRad(endLong - startLong);
    let startLatRad = toRad(startLat);
    let endLatRad = toRad(endLat);

    let a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.sin(dLon / 2) * Math.sin(dLon / 2) * Math.cos(startLatRad) * Math.cos(endLatRad);
    let c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    let d = R * c;
    let distance_element = document.getElementById(elementID);
    distance_element.innerHTML = d.toFixed(1);
}

// Converts numeric degrees to radians
function toRad(Value) {
    return Value * Math.PI / 180;
}
