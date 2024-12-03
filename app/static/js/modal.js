// app/static/js/modal.js

document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('mobileModal');
    const closeButton = modal.querySelector('.close-button');

    function showModal() {
        modal.style.display = 'block';
    }

    function hideModal() {
        modal.style.display = 'none';
        localStorage.setItem('modalClosed', 'true');
    }

    function checkViewport() {
        const isModalClosed = localStorage.getItem('modalClosed');
        if (window.innerWidth < 768 && !isModalClosed) {
            showModal();
        } else {
            hideModal();
        }
    }

    checkViewport(); // Perform initial viewport check

    closeButton.addEventListener('click', hideModal);

    window.addEventListener('click', function (event) {
        if (event.target === modal) {
            hideModal();
        }
    });

    window.addEventListener('resize', checkViewport); // Update modal visibility on resize
});
