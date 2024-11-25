document.addEventListener('DOMContentLoaded', function () {
    // Selecciona todos los elementos <a> con la clase 'project-link'
    const projectLinks = document.querySelectorAll('.project-link');
    
    // Selecciona los elementos del preview
    const previewContainer = document.getElementById('project-preview');
    const previewImage = document.querySelector('.project-preview-image');
    const previewTitle = document.getElementById('preview-title');
    const previewDescription = document.getElementById('preview-description');

    projectLinks.forEach(link => {
        // Evento cuando el mouse entra en el <a>
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

        // Evento para seguir la posición del mouse
        link.addEventListener('mousemove', function (e) {
            const previewWidth = previewContainer.offsetWidth;
            const previewHeight = previewContainer.offsetHeight;
            const pageWidth = window.innerWidth;
            const pageHeight = window.innerHeight;

            let x = e.pageX + 15; // Margen de 15px a la derecha
            let y = e.pageY + 15; // Margen de 15px abajo

            // Ajusta la posición si el preview se sale de la pantalla
            if (x + previewWidth > pageWidth) {
                x = e.pageX - previewWidth - 15;
            }
        
            if (y + previewHeight > pageHeight) {
                y = pageHeight - previewHeight - 15;
            }

            previewContainer.style.left = `${x}px`;
            previewContainer.style.top = `${y}px`;
        });

        // Evento cuando el mouse sale del <a>
        link.addEventListener('mouseleave', function () {
            previewContainer.classList.remove('visible');
            previewContainer.style.display = 'none';
        });

        // Evento click en el <a>
        link.addEventListener('click', function (e) {
            const projectLink = link.getAttribute('href');
            if (projectLink && projectLink !== '#') {
                window.location.href = projectLink;
            } else {
                e.preventDefault(); // Evita la acción predeterminada si el enlace es '#'
            }
        });
    });
});