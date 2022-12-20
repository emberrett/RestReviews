
document.getElementById("test").innerHTML = "yeehaw";

function submitSearch(event) {
    if (event.key == 'Enter') {
        let baseURL = window.location.origin + "/my-rests";
        let url = new URL(baseURL);
        let searchQuery = document.getElementById('rest_search').value;
        url.searchParams.set('search', searchQuery);
        window.location.assign(url);

    }

}
