let darkmode = localStorage.getItem('darkmode');
const themeSwitch = document.getElementById('theme-switch');

document.getElementById('theme-switch').addEventListener('click', function() {
    this.classList.add('clicked');
    setTimeout(() => {
        this.classList.remove('clicked');
    }, 500); // Match the duration of the transition
});

const enableDarkMode = () => {
    document.body.classList.add('darkmode');
    localStorage.setItem('darkmode', 'active');
}

const disableDarkMode = () => {
    document.body.classList.remove('darkmode');
    localStorage.setItem('darkmode', null);
}

if(darkmode === "active") enableDarkMode();

themeSwitch.addEventListener("click", () => {
    darkmode = localStorage.getItem('darkmode'); // Update the value of darkmode
    darkmode !== "active" ? enableDarkMode() : disableDarkMode();
});