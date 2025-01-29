// app/static/js/scripts.js

document.addEventListener('DOMContentLoaded', function() {
    const invertToggle = document.getElementById('invertToggle');
    const avatarImages = document.querySelectorAll('.invertible-image'); 
    const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");

    function applyColorScheme() {
        const savedPreference = localStorage.getItem("colorScheme");
        if (savedPreference === "inverted") {
            document.body.classList.add('inverted');
            avatarImages.forEach(img => {
                img.src = img.getAttribute('data-inverted-src');
            });
            invertToggle.checked = true;
        } else if (savedPreference === "default") {
            document.body.classList.remove('inverted');
            avatarImages.forEach(img => {
                img.src = img.getAttribute('data-default-src');
            });
            invertToggle.checked = false;
        } else {
            // Aplicar invertido por defecto
            document.body.classList.add('inverted');
            avatarImages.forEach(img => {
                img.src = img.getAttribute('data-inverted-src');
            });
            invertToggle.checked = true;
        }
    }

    applyColorScheme();

    invertToggle.addEventListener('change', function() {
        if (invertToggle.checked) {
            document.body.classList.add('inverted');
            avatarImages.forEach(img => {
                img.src = img.getAttribute('data-inverted-src');
            });
            localStorage.setItem("colorScheme", "inverted");
        } else {
            document.body.classList.remove('inverted');
            avatarImages.forEach(img => {
                img.src = img.getAttribute('data-default-src');
            });
            localStorage.setItem("colorScheme", "default");
        }
    });
});