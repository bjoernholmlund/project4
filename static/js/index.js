/*hammenu*/
const hamMenu = document.querySelector('.ham-menu');
const offScreenMenu = document.querySelector('.off-screen-menu');

hamMenu.addEventListener('click', () => {
    hamMenu.classList.toggle('active');
    offScreenMenu.classList.toggle('active');
})

/*-------*/
/*modal - reservation button and form*/
function openPopup() {
    document.getElementById("popup").style.display = "flex";
}

function closePopup() {
    document.getElementById("popup").style.display = "none";
}

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("popup").style.display = "none"; // Tvinga att det är dolt vid start
});

// Stänger popup om användaren klickar utanför
window.onclick = function(event) {
    let popup = document.getElementById("popup");
    if (event.target == popup) {
        closePopup();
    }
};