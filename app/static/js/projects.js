// app/static/js/projects.js

document.addEventListener('DOMContentLoaded', function () {
    const projectLefts = document.querySelectorAll('.project-left');
    const previewContainer = document.getElementById('project-preview');
    const previewImage = document.querySelector('.project-preview-image');
    const previewTitle = document.getElementById('preview-title');
    const previewDescription = document.getElementById('preview-description');

    let isMouseOverProjectLeft = false;
    let isMouseOverPreview = false;

    function showPreview(link) {
        const projectTitle = link.getAttribute('data-title');
        const projectDescription = link.getAttribute('data-description');
        const projectImage = link.getAttribute('data-image');

        if (projectImage && projectTitle && projectDescription) {
            previewImage.src = projectImage;
            previewImage.alt = `${projectTitle} Preview`;
            previewTitle.textContent = projectTitle;
            previewDescription.textContent = projectDescription;
            previewContainer.style.display = 'block';
            setTimeout(() => {
                previewContainer.classList.add('visible');
            }, 10);
        }
    }

    function hidePreview() {
        previewContainer.classList.remove('visible');
        previewContainer.addEventListener('transitionend', function handler(event) {
        }, { once: true });
    }

    function movePreview(e, container) {
        const previewWidth = previewContainer.offsetWidth;
        const previewHeight = previewContainer.offsetHeight;
        const containerRect = container.getBoundingClientRect();
        const containerWidth = container.offsetWidth;
        const containerHeight = container.offsetHeight;

        let x = e.clientX - containerRect.left + 15;
        let y = e.clientY - containerRect.top + 15;

        if (x + previewWidth > containerWidth) {
            x = e.clientX - containerRect.left - previewWidth - 15;
        }

        if (y + previewHeight > containerHeight) {
            y = e.clientY - containerRect.top - previewHeight - 15;
        }

        previewContainer.style.left = `${x}px`;
        previewContainer.style.top = `${y}px`;
    }

    projectLefts.forEach(left => {
        const link = left.querySelector('.project-link');
        if (!link) return;

        left.addEventListener('mouseenter', function (e) {
            isMouseOverProjectLeft = true;
            showPreview(link);
        });

        left.addEventListener('mousemove', function (e) {
            const container = document.querySelector('.personal-projects');
            movePreview(e, container);
        });

        left.addEventListener('mouseleave', function () {
            isMouseOverProjectLeft = false;
            if (!isMouseOverPreview) {
                hidePreview();
            }
        });

        link.addEventListener('click', function (e) {
            const projectLink = link.getAttribute('href');
            if (projectLink && projectLink !== '#') {
                window.location.href = projectLink;
            } else {
                e.preventDefault();
            }
        });
    });

    previewContainer.addEventListener('mouseenter', function() {
        isMouseOverPreview = true;
    });

    previewContainer.addEventListener('mouseleave', function() {
        isMouseOverPreview = false;
        if (!isMouseOverProjectLeft) {
            hidePreview();
        }
    });
});