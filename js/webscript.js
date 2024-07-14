// const langs = require('./lang.json');
// console.log(langs);

function launch() {
    // (onload function for main index)
    // populate the dropdown menu with correct languages
    // generateIndex
    return;
}


/*  */
function configureDropdownLinks(doi) {
    // params: doi, lang
    // called from index or another article page
    // configure the dropdown langs to have data-doi = doi
    console.log(document);
    let dropdown = document.getElementById("lang-dropdown");
    console.log(dropdown);
    let els = dropdown.getElementsByTagName("*");
    for (let i = 0; i < els.length; i++) {
        let newlink = "";
        if (doi === "index") {
            newlink = "/lang/" + els[i].getAttribute("id") + "/index.html";
        }
        else {
            newlink = "/lang/" + els[i].getAttribute("id") + "/" + doi + ".xml";
        }
        els[i].setAttribute("href", newlink);
        console.log(newlink); // debugging
    }
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