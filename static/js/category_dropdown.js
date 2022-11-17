const categoryText = document.getElementById('category_text');
const categoryDropdown = document.getElementById('category_dropdown');

function handleRadioClick() {
    if (document.getElementById('category_dropdown_radio').checked) {
        categoryText.required = false;
        categoryText.disabled = true;
        categoryDropdown.disabled = false;

    } else {
        categoryText.required = true;
        categoryText.disabled = false;
        categoryDropdown.disabled = true;
    }
}

const radioButtons = document.getElementsByClassName("category_radio");
Array.from(radioButtons).forEach(radio => {
    radio.addEventListener('click', handleRadioClick);
});

handleRadioClick()