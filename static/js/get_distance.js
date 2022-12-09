var startLong = parseFloat((new URL(document.location)).searchParams.get("startLong"));
var startLat = parseFloat((new URL(document.location)).searchParams.get("startLat"));

function calcCrow(elementID, endLat, endLong, km=false) {
    let distance_element = document.getElementById(elementID);
    if (startLong && startLat) {
        let distanceHeader = document.getElementById("distance");
        distanceHeader.classList.add("sortable-columns");
        if (km===false) {
            let R = 6378; // km
        }
        else {
            let R = 3963; //m
        }
        let R = 3963;
        let dLat = toRad(endLat - startLat);
        let dLon = toRad(endLong - startLong);
        let startLatRad = toRad(startLat);
        let endLatRad = toRad(endLat);
    
        let a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.sin(dLon / 2) * Math.sin(dLon / 2) * Math.cos(startLatRad) * Math.cos(endLatRad);
        let c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        let d = R * c;
        distance_element.innerHTML = d.toFixed(1).concat("mi");

    }
    else {  
        distance_element.innerHTML = null;

    }
}

// Converts numeric degrees to radians
function toRad(Value) {
    return Value * Math.PI / 180;
}
