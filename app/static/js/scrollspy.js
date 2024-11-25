document.addEventListener("DOMContentLoaded", function() {
    const sections = document.querySelectorAll("div[id]");
    const navLinks = document.querySelectorAll(".components .nav-link");

    function changeActiveLink() {
        let currentSectionId = '';
        sections.forEach((section) => {
            const rect = section.getBoundingClientRect();
            if (rect.top <= window.innerHeight / 2 && rect.bottom >= window.innerHeight / 2) {
                currentSectionId = section.id;
            }
        });

        navLinks.forEach((link) => link.classList.remove('active'));
        if (currentSectionId) {
            const activeLink = document.querySelector(`.components .nav-link[href="#${currentSectionId}"]`);
            if (activeLink) {
                activeLink.classList.add('active');
            }
        }
    }

    window.addEventListener('scroll', changeActiveLink);
    changeActiveLink(); // Llamada inicial
});