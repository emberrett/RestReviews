
function getPage() {
    let pageParam = (new URL(document.location)).searchParams.get("page");
    if (pageParam == null) {
        pageParam = 1;
    }
    else {
        pageParam = parseInt(pageParam);
    }
    return pageParam;
}

function setNextButton() {
    const nextButton = document.getElementById("next_button");
    if (nextButton != null) {
        let url = new URL(window.location.href);
        url.searchParams.set('page', getPage() + 1);
        nextButton.href = url;
    }
}

function setBackButton() {
    const backButton = document.getElementById("back_button");
    if (backButton != null) {
        let url2 = new URL(window.location.href);
        url2.searchParams.set('page', getPage() - 1);
        backButton.href = url2;
    }
}

setNextButton();
setBackButton();