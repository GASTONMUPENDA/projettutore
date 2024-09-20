window.onscroll = function() {scrollFunction()};

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        document.querySelector(".retour_haut").style.display = "block";
    } else {
        document.querySelector(".retour_haut").style.display = "none";
    }
}

document.querySelector(".retour_haut").onclick = function() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}
