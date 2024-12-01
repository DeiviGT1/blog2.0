// app/static/js/modal.js

document.addEventListener("DOMContentLoaded", function() {
    // Función para determinar si el dispositivo es móvil basado en el userAgent y ancho de ventana
    function isMobileDevice() {
        return /Mobi|Android|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) && window.innerWidth <= 768;
    }

    // Obtener elementos del DOM
    var modal = document.getElementById("mobileModal");
    var closeButton = document.querySelector(".close-button");

    // Función para mostrar el modal
    function showModal() {
        modal.style.display = "flex";
        modal.classList.add("show");
        // Establecer el foco en el contenido del modal para accesibilidad
        modal.querySelector('.modal-content').focus();
    }

    // Función para ocultar el modal
    function hideModal() {
        modal.style.display = "none";
        modal.classList.remove("show");
        // Marcar que el modal ha sido mostrado y cerrado por el usuario
        localStorage.setItem('mobileModalClosed', 'true');
    }

    // Mostrar el modal si es dispositivo móvil y el usuario no lo ha cerrado antes
    if (isMobileDevice() && !localStorage.getItem('mobileModalClosed')) {
        showModal();
    }

    // Cerrar el modal al hacer clic en el botón de cerrar
    closeButton.addEventListener("click", hideModal);

    // Cerrar el modal al hacer clic fuera del contenido del modal
    window.addEventListener("click", function(event) {
        if (event.target == modal) {
            hideModal();
        }
    });

    // Opcional: Cerrar el modal al presionar la tecla Esc
    window.addEventListener("keydown", function(event) {
        if (event.key === "Escape") {
            hideModal();
        }
    });

    // Opcional: Manejar rotación de pantalla
    window.addEventListener("resize", function() {
        if (!isMobileDevice()) {
            hideModal();
        }
    });
});