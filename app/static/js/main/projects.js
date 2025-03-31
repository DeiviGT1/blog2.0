document.addEventListener('DOMContentLoaded', function () {
    const projectLinks = document.querySelectorAll('.project-link');
  
    const previewContainer = document.getElementById('project-preview');
    const previewImage = previewContainer.querySelector('.project-preview-image');
    const previewTitle = document.getElementById('preview-title');
    const previewDescription = document.getElementById('preview-description');
  
    /*Muestra el preview con la información del proyecto.*/
    function showPreview(link) {
      const projectTitle = link.getAttribute('data-title');
      const projectDescription = link.getAttribute('data-description');
      const projectImage = link.getAttribute('data-image');
  
      previewImage.src = projectImage || '';
      previewImage.alt = (projectTitle || 'Project') + ' Preview';
      previewTitle.textContent = projectTitle || 'Untitled Project';
      previewDescription.textContent = projectDescription || 'No description provided.';
  
      previewContainer.style.display = 'block';
    }
  
    function hidePreview() {
      previewContainer.style.display = 'none';
    }
  
    /*Ajusta la posición del contenedor de preview para que siga el ratón.*/
    function positionPreview(e) {
      const offset = 10;
      // Obtenemos las dimensiones actuales del preview
      const previewRect = previewContainer.getBoundingClientRect();
    
      // Posicionamos en X de forma similar a lo que ya tenías
      let x = e.pageX + offset;
      if (x + previewRect.width > window.innerWidth) {
        x = e.pageX - previewRect.width - offset;
      }
    
      // Para la posición vertical usamos clientY, que da la posición dentro del viewport
      let y;
      // Si hay suficiente espacio debajo del cursor, mostramos el preview abajo
      if (e.clientY + previewRect.height + offset < window.innerHeight) {
        y = e.pageY + offset;
      } else {
        // Si no, lo mostramos arriba del cursor
        y = e.pageY - previewRect.height - offset;
      }
    
      previewContainer.style.left = x + 'px';
      previewContainer.style.top = y + 'px';
    }
  
    // Para cada enlace de proyecto
    projectLinks.forEach(link => {
      link.addEventListener('mouseenter', function () {
        showPreview(link);
      });
  
      link.addEventListener('mousemove', function (e) {
        positionPreview(e);
      });
  
      link.addEventListener('mouseleave', function () {
        hidePreview();
      });
    });
  });