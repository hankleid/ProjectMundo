const langs = require('./lang.json');
console.log(langs);

/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function dropDown() {
    document.getElementById("lang-dropdown").classList.toggle("show");
}

/* Refresh page when a navbar dropdown language is selected */
function switchLang() {
    document.getElementById("lang-dropdown").classList.toggle("show");
}

/* Update the links in the navbar dropdown */
function populateLangLinks() {
    document.getElementById("lang-dropdown").classList.toggle("show");
}
  
// Close the dropdown if the user clicks outside of it
window.onclick = function(e) {
if (!e.target.matches('.dropbtn')) {
var myDropdown = document.getElementById("lang-dropdown");
    if (myDropdown.classList.contains('show')) {
    myDropdown.classList.remove('show');
    }
}
}