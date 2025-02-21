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

// Vänta tills sidan har laddats helt
window.onload = function() {
    // Sätt en fördröjning innan texten blir synlig
    setTimeout(function() {
        // Lägg till 'hidden' klassen som triggar animationen
        document.getElementById('delayed-text').classList.remove('hidden');
        document.getElementById('delayed-text').classList.add('visible');
    }, 1000); // Fördröjningen innan animationen startar
};