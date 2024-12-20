// app/static/js/video.js

document.addEventListener("DOMContentLoaded", () => {
  const videoOverlay = document.getElementById("video-overlay");
  const videoPlayer = document.getElementById("video-player");
  const closeVideo = document.getElementById("close-video");

  document
    .querySelector(".project-link[data-project='5']")
    .addEventListener("click", (event) => {
      event.preventDefault();
      const videoUrl = event.target.closest(".project-link").dataset.video;
      videoPlayer.src = videoUrl; // Asigna la URL del video
      videoOverlay.classList.remove("hidden");
    });

  closeVideo.addEventListener("click", () => {
    videoOverlay.classList.add("hidden");
    videoPlayer.pause(); // Pausa el video
    videoPlayer.src = ""; // Limpia el src del video
  });
});