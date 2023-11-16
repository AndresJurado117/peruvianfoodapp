document.addEventListener("DOMContentLoaded", function() {
    document.querySelector("search").addEventListener("input", function(event) {
        const searchTerm = event
    });
})

const searchWrapper = document.querySelector(".button-container");
const inputBox = searchWrapper.querySelector("input");
const suggestionBox = searchWrapper.querySelector("autocomplete");
let linkTag = searchWrapper.querySelector("a");
let webLink;

inputBox.onkeyup = (e) => {
    let userData = e.target.value;
    let emptyArray = [];
    if (userData) {

    } else {
        searchWrapper.classList.remove("active");
    }
}