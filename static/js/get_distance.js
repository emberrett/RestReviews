var startLong = parseFloat((new URL(document.location)).searchParams.get("startLong"));
var startLat = parseFloat((new URL(document.location)).searchParams.get("startLat"));
function calcDistance(elementID, endLat, endLong, miles = "True") {
    let distance_element = document.getElementById(elementID);
    if (startLong && startLat) {
        let distanceHeader = document.getElementById("distance");
        distanceHeader.classList.add("sortable-columns");
        if (miles == "False") {
            var R = 6378; // km
            measurement = "km";
        }
        else {
            var R = 3963; //m
            measurement = "mi";
        }
        let dLat = toRad(endLat - startLat);
        let dLon = toRad(endLong - startLong);
        let startLatRad = toRad(startLat);
        let endLatRad = toRad(endLat);

        let a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.sin(dLon / 2) * Math.sin(dLon / 2) * Math.cos(startLatRad) * Math.cos(endLatRad);
        let c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        let d = R * c;

        distance_element.innerHTML = d.toFixed(1).concat(measurement);

    }
    else {
        distance_element.innerHTML = null;

    }
}

// Converts numeric degrees to radians
function toRad(Value) {
    return Value * Math.PI / 180;
}
