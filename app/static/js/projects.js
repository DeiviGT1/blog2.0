// app/static/js/projects.js

document.addEventListener('DOMContentLoaded', function () {
    // Seleccionar todos los elementos <div> con clase 'project-left'
    const projectLefts = document.querySelectorAll('.project-left');
    
    // Seleccionar elementos de previsualización
    const previewContainer = document.getElementById('project-preview');
    const previewImage = document.querySelector('.project-preview-image');
    const previewTitle = document.getElementById('preview-title');
    const previewDescription = document.getElementById('preview-description');

    // Función para mostrar la previsualización
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
            // Usamos una ligera demora para activar la transición CSS
            setTimeout(() => {
                previewContainer.classList.add('visible');
            }, 10);
        }
    }

    // Función para ocultar la previsualización
    function hidePreview() {
        previewContainer.classList.remove('visible');
        // Usar { once: true } para asegurar que el listener se ejecuta solo una vez
        previewContainer.addEventListener('transitionend', function handler(event) {
            // Asegurarse de que la transición que terminó es la de la opacidad
            if (event.propertyName === 'opacity') {
                previewContainer.style.display = 'none';
            }
        }, { once: true });
    }

    // Función para mover la previsualización
    function movePreview(e, container) {
        const previewWidth = previewContainer.offsetWidth;
        const previewHeight = previewContainer.offsetHeight;
        const containerRect = container.getBoundingClientRect();
        const containerWidth = container.offsetWidth;
        const containerHeight = container.offsetHeight;

        // Calcular la posición del ratón relativa al contenedor
        let x = e.clientX - containerRect.left + 15; // Margen de 15px a la derecha
        let y = e.clientY - containerRect.top + 15;  // Margen de 15px abajo

        // Ajustar la posición si la previsualización se sale del contenedor horizontalmente
        if (x + previewWidth > containerWidth) {
            x = e.clientX - containerRect.left - previewWidth - 15;
        }

        // Ajustar la posición si la previsualización se sale del contenedor verticalmente
        if (y + previewHeight > containerHeight) {
            y = e.clientY - containerRect.top - previewHeight - 15;
        }

        previewContainer.style.left = `${x}px`;
        previewContainer.style.top = `${y}px`;
    }

    // Añadir eventos a cada <div> de project-left
    projectLefts.forEach(left => {
        const link = left.querySelector('.project-link');

        // Verificar que el <a> existe
        if (!link) return;

        // Evento cuando el ratón entra al .project-left
        left.addEventListener('mouseenter', function (e) {
            showPreview(link);
        });

        // Evento para seguir la posición del ratón
        left.addEventListener('mousemove', function (e) {
            const container = document.querySelector('.personal-projects');
            movePreview(e, container);
        });

        // Evento cuando el ratón sale del .project-left
        left.addEventListener('mouseleave', function () {
            hidePreview();
        });

        // Evento de clic en el <a>
        link.addEventListener('click', function (e) {
            const projectLink = link.getAttribute('href');
            if (projectLink && projectLink !== '#') {
                window.location.href = projectLink;
            } else {
                e.preventDefault(); // Prevenir acción por defecto si el enlace es '#'
            }
        });
    });
});