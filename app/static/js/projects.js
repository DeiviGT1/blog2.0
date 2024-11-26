// app/static/js/projects.js

document.addEventListener('DOMContentLoaded', function () {
    // Select all <a> elements with class 'project-link'
    const projectLinks = document.querySelectorAll('.project-link');
    
    // Select preview elements
    const previewContainer = document.getElementById('project-preview');
    const previewImage = document.querySelector('.project-preview-image');
    const previewTitle = document.getElementById('preview-title');
    const previewDescription = document.getElementById('preview-description');

    // Get the bounding rectangle of the container
    const container = document.querySelector('.personal-projects');
    const containerRect = container.getBoundingClientRect();

    projectLinks.forEach(link => {
        // Event when the mouse enters the <a>
        link.addEventListener('mouseenter', function (e) {
            const projectTitle = link.getAttribute('data-title');
            const projectDescription = link.getAttribute('data-description');
            const projectImage = link.getAttribute('data-image');

            if (projectImage && projectTitle && projectDescription) {
                previewImage.src = projectImage;
                previewImage.alt = `${projectTitle} Preview`;
                previewTitle.textContent = projectTitle;
                previewDescription.textContent = projectDescription;
                previewContainer.style.display = 'block';
                previewContainer.classList.add('visible');
            }
        });

        // Event to follow the mouse position
        link.addEventListener('mousemove', function (e) {
            const previewWidth = previewContainer.offsetWidth;
            const previewHeight = previewContainer.offsetHeight;
            const containerWidth = container.offsetWidth;
            const containerHeight = container.offsetHeight;

            // Calculate mouse position relative to the container
            let x = e.clientX - containerRect.left + 15; // Margin of 15px to the right
            let y = e.clientY - containerRect.top + 15;  // Margin of 15px below

            // Adjust the position if the preview goes off-screen horizontally
            if (x + previewWidth > containerWidth) {
                x = e.clientX - containerRect.left - previewWidth - 15;
            }

            // Adjust the position if the preview goes off-screen vertically
            if (y + previewHeight > containerHeight) {
                y = e.clientY - containerRect.top - previewHeight - 15;
            }

            previewContainer.style.left = `${x}px`;
            previewContainer.style.top = `${y}px`;
        });

        // Event when the mouse leaves the <a>
        link.addEventListener('mouseleave', function () {
            previewContainer.classList.remove('visible');
            previewContainer.style.display = 'none';
        });

        // Click event on the <a>
        link.addEventListener('click', function (e) {
            const projectLink = link.getAttribute('href');
            if (projectLink && projectLink !== '#') {
                window.location.href = projectLink;
            } else {
                e.preventDefault(); // Prevent default action if the link is '#'
            }
        });
    });
    
});