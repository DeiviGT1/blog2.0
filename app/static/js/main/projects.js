document.addEventListener('DOMContentLoaded', function () {
    // Seleccionamos todos los enlaces de proyectos
    const projectLinks = document.querySelectorAll('.project-link');
  
    // Selección del contenedor de preview y sus elementos
    const previewContainer = document.getElementById('project-preview');
    const previewImage = previewContainer.querySelector('.project-preview-image');
    const previewTitle = document.getElementById('preview-title');
    const previewDescription = document.getElementById('preview-description');
  
    /**
     * Muestra el preview con la información del proyecto.
     */
    function showPreview(link) {
      const projectTitle = link.getAttribute('data-title');
      const projectDescription = link.getAttribute('data-description');
      const projectImage = link.getAttribute('data-image');
  
      previewImage.src = projectImage || '';
      previewImage.alt = (projectTitle || 'Project') + ' Preview';
      previewTitle.textContent = projectTitle || 'Untitled Project';
      previewDescription.textContent = projectDescription || 'No description provided.';
  
      // Mostramos el contenedor (sin animaciones, directamente)
      previewContainer.style.display = 'block';
    }
  
    /**
     * Oculta el preview inmediatamente.
     */
    function hidePreview() {
      previewContainer.style.display = 'none';
    }
  
    /**
     * Ajusta la posición del contenedor de preview para que siga el ratón.
     * @param {MouseEvent} e
     */
    function positionPreview(e) {
      const offsetX = 10; // Ajusta a tu gusto
      const offsetY = 10;
  
      // Usamos pageX/pageY para considerar el scroll vertical
      let x = e.pageX + offsetX;
      let y = e.pageY + offsetY;
  
      const containerWidth = previewContainer.offsetWidth;
      const containerHeight = previewContainer.offsetHeight;
  
      // Ajustar para no salirse por la derecha
      if (x + containerWidth > document.documentElement.clientWidth) {
        x = e.pageX - containerWidth - offsetX;
      }
      // Ajustar para no salirse por debajo
      if (y + containerHeight > document.documentElement.clientHeight) {
        y = e.pageY - containerHeight - offsetY;
      }
  
      previewContainer.style.left = x + 'px';
      previewContainer.style.top = y + 'px';
    }
  
    // Para cada enlace de proyecto
    projectLinks.forEach(link => {
      // Al poner el mouse sobre el enlace
      link.addEventListener('mouseenter', function () {
        showPreview(link);
      });
  
      // Al mover el mouse dentro del enlace, actualizamos la posición
      link.addEventListener('mousemove', function (e) {
        positionPreview(e);
      });
  
      // Al salir del enlace, ocultamos el preview inmediatamente
      link.addEventListener('mouseleave', function () {
        hidePreview();
      });
    });
  });