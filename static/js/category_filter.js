

function toggle(source) {
    let checkboxes = document.getElementsByName('category_list');
    for (var i = 0, n = checkboxes.length; i < n; i++) {
        checkboxes[i].checked = source.checked;
    }
    setCategories()
}
function loadCategories() {
    let url = new URL(window.location.href);

    let categoryParams = (new URL(document.location)).searchParams.get("categories");


    if (categoryParams) {
        let currentCategoryArray = categoryParams.split(',');

        for (var i = 0, n = currentCategoryArray.length; i < n; i++) {
            category_id = "cat_" + currentCategoryArray[i];
            let categoryCheckBox = document.getElementById(category_id);
            categoryCheckBox.checked = true;
            document.getElementById("select_all").checked = false;

        }

    }

    else {
        let checkboxes = document.getElementsByName('category_list');
        Array.from(checkboxes).forEach(checkbox => {
            checkbox.checked = true;
        })
        document.getElementById("select_all").checked = true;


    }
}
function setCategories() {

    let url = new URL(window.location.href);
    let checkboxes = document.getElementsByName('category_list');
    let categoryArray = [];



    let selectAllBox = document.getElementById("select_all");


    selectAllBox.checked = true;
    noneChecked = true;
    Array.from(checkboxes).forEach(checkbox => {
        if (checkbox.value != "select_all") {
            if (checkbox.checked === true) {
                noneChecked = false;
                categoryArray.push(checkbox.value);
            }
            else {
                selectAllBox.checked = false;
            }
        }
    });


    if (selectAllBox.checked === true) {
        url.searchParams.delete('categories');
    }
    else if (noneChecked) {
        url.searchParams.set('categories', "none");

    }
    else {
        url.searchParams.set('categories', categoryArray.join(","));
    }
    window.location.assign(url);
}
