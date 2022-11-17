const slider = document.getElementById('my_rating');
const sliderValue = document.getElementById('range_value')
const sliderDiv = document.getElementById('slider_div')
function handleTriedRadio() {
    if (document.getElementById('tried_true').checked) {

      slider.setAttribute("max",5);
      sliderDiv.classList.remove("slider-disabled");
      sliderValue.innerHTML = slider.value;
       
    } else {
        slider.setAttribute("max",0);
        slider.setAttribute("value",0);
        sliderDiv.classList.add("slider-disabled");
        sliderValue.innerHTML = "0"
    }
}

const triedRadios = document.getElementsByClassName("tried_radio");
Array.from(triedRadios).forEach(radio => {
    radio.addEventListener('click', handleTriedRadio);
});


handleTriedRadio()