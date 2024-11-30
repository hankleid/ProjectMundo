function configureDropdown(doi, lang) {
    // params: doi, lang
    // called from index or another article page
    // configure the dropdown langs to have data-doi = doi
    // update the dropdown button with the current language

    console.log(lang)
    fetch('/lang.json')
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            let dropdown_button = document.getElementById("btn-dropdown");
            dropdown_button.textContent = data.codes[lang];
        });

    let dropdown = document.getElementById("lang-dropdown");
    let els = dropdown.getElementsByTagName("*");
    for (let i = 0; i < els.length; i++) {
        let newlink = "";
        if (doi === "index") {
            newlink = "/index/" + els[i].getAttribute("id") + ".html";
        }
        else {
            newlink = "/articles/" + doi + "/" + els[i].getAttribute("id") + ".xml";
        }
        els[i].setAttribute("href", newlink);
    }
    
    let home = document.getElementById("home");
    home.setAttribute("href", "/index/" + lang + ".html")
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