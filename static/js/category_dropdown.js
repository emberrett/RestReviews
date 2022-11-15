const category_text = document.getElementById('category_text');
const category_dropdown = document.getElementById('category_dropdown');

function handleRadioClick() {
    if (document.getElementById('category_dropdown_radio').checked) {

        category_text.required = false;
        category_text.disabled = true;
        category_dropdown.disabled = false;

    } else {
        category_text.required = true;
        category_text.disabled = false;
        category_dropdown.disabled = true;
    }
}

const radioButtons = document.getElementsByClassName("category_radio");
Array.from(radioButtons).forEach(radio => {
    radio.addEventListener('click', handleRadioClick);
});
