document.addEventListener("DOMContentLoaded", function () {
    const rotatingCard = document.querySelector(".rotating-card");

    window.addEventListener("scroll", function () {
        const scrollTop = window.scrollY;
        const documentHeight = document.documentElement.scrollHeight - window.innerHeight;
        let scrollPercentage = 0;

        if (documentHeight > 0) {
            scrollPercentage = scrollTop / documentHeight;
        }

        const rotationAngle = scrollPercentage * 180;
        rotatingCard.style.transform = `rotateY(${rotationAngle}deg)`;
    });
});