// app/static/js/scripts.js

document.addEventListener('DOMContentLoaded', function() {
    const invertToggle = document.getElementById('invertToggle');
    const avatarImages = document.querySelectorAll('.invertible-image'); // Seleccionar todas las imágenes invertibles
    const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");

    // Función para aplicar el esquema de colores
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

    // Aplicar el esquema de colores al cargar la página
    applyColorScheme();

    // Escuchar el cambio en el toggle para invertir colores
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