const langs = require('./lang.json');
console.log(langs);

function launch() {
    // (onload function for main index)
    // populate the dropdown menu with correct languages
    // generateIndex
    return;
}

/*  */
function generateIndex() {
    // param: lang
    // generate links to all the dois in the lang specified
    // elements should have id = doi; data-lang = lang
    return;
}

/*  */
function retrieveArticle() {
    // params: doi, lang
    // called from index or another article page
    // configure the dropdown langs to have data-doi = doi
    return;
}

/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function dropDown() {
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