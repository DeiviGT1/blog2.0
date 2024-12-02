// app/static/js/modal.js

document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('mobileModal');
    const closeButton = modal.querySelector('.close-button');

    // Function to show the modal
    function showModal() {
        modal.style.display = 'block';
    }

    // Function to hide the modal and set the flag in localStorage
    function hideModal() {
        modal.style.display = 'none';
        localStorage.setItem('modalClosed', 'true'); // Set the flag
    }

    // Function to check viewport width and toggle modal
    function checkViewport() {
        const isModalClosed = localStorage.getItem('modalClosed');
        if (window.innerWidth < 768 && !isModalClosed) {
            showModal();
        } else {
            hideModal();
        }
    }

    // Initial check on page load
    checkViewport();

    // Event listener for the close button
    closeButton.addEventListener('click', hideModal);

    // Hide modal when clicking outside the modal content
    window.addEventListener('click', function (event) {
        if (event.target === modal) {
            hideModal();
        }
    });

    // Optional: Listen for window resize events to toggle modal dynamically
    window.addEventListener('resize', checkViewport);
});