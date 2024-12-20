// app/static/js/video.js

document.addEventListener("DOMContentLoaded", () => {
  const videoOverlay = document.getElementById("video-overlay");
  const videoPlayer = document.getElementById("video-player");
  const closeVideo = document.getElementById("close-video");

  // Selecciona todos los elementos con clase 'project-link' y data-project='5' o '3'
  const projectLinks = document.querySelectorAll(".project-link[data-project='5'], .project-link[data-project='3']");

  // Verifica si hay elementos seleccionados
  if (projectLinks.length > 0) {
    projectLinks.forEach((link) => {
      link.addEventListener("click", (event) => {
        event.preventDefault();
        const videoUrl = link.dataset.video; // Obtiene el valor de 'data-video'
        
        if (videoUrl) { // Verifica que 'data-video' exista
          videoPlayer.src = videoUrl; // Asigna la URL del video
          videoOverlay.classList.remove("hidden");
          videoPlayer.play(); // Opcional: Inicia la reproducción automática
        } else {
          console.error("La URL del video no está definida para este enlace.");
        }
      });
    });
  } else {
    console.warn("No se encontraron elementos .project-link con data-project='5' o '3'.");
  }

  // Maneja el evento de cierre del video
  if (closeVideo) {
    closeVideo.addEventListener("click", () => {
      videoOverlay.classList.add("hidden");
      videoPlayer.pause(); // Pausa el video
      videoPlayer.src = ""; // Limpia el src del video
    });
  } else {
    console.warn("Elemento con ID 'close-video' no encontrado.");
  }
});