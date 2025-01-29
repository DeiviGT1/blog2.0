// app/static/js/playlist.js

document.addEventListener("DOMContentLoaded", function() {
  // Select the element with ID 'playlist-data'
  var playlistDataElement = document.getElementById('playlist-data');
  if (!playlistDataElement) {
    console.error("Element with ID 'playlist-data' not found.");
    return;
  }


  var dataBase64 = playlistDataElement.getAttribute('data-playlist');
  if (!dataBase64) {
    console.error('El atributo data-playlist está vacío');
    return;
  }
  var dataJson;
  try {
    dataJson = atob(dataBase64);
  } catch (e) {
    console.error('Error decodificando Base64:', e);
    return;
  }

  var data;
  try {
    data = JSON.parse(dataJson);
  } catch (e) {
    console.error('Error parseando JSON:', e);
    return;
  }

  if (!data || data.length === 0) {
    console.error('No se encontraron datos de playlists.');
    var playlistContainer = document.getElementById("playlist");
    playlistContainer.innerHTML = "<p>No se encontraron playlists con canciones.</p>";
    return;
  }
  
  var playlistContainer = document.getElementById("playlist");
  var list = document.createElement("ul");

  for (var i = 0; i < data.length; i++) {
    var playlist_name = data[i].playlist_name;
    var playlist_url = data[i].playlist_url;
    var average_popularity = parseFloat(data[i].avg_popularity);

    var Comentario;
    if (average_popularity > 70){
      Comentario = 'Esta playlist es increíble. ¡Tienes muy buen gusto musical! Cada canción es una joya.';
    } else if (average_popularity > 55){
      Comentario = 'Esta playlist es muy buena. Tiene una variedad de estilos y ritmos que te hacen disfrutar de la música.';
    } else if (average_popularity > 45){
      Comentario = 'Esta playlist es decente. Tiene un equilibrio entre canciones populares y otras más desconocidas.';
    } else if (average_popularity > 20){
      Comentario = 'Esta playlist no es muy atractiva. Tiene algunas canciones buenas, pero otras que no pegan nada.';
    } else {
      Comentario = 'Esta playlist necesita una renovación urgente. Tal vez deberías explorar otros géneros musicales.';
    }

    localStorage.setItem('playlistData', dataJson);

    var listItem = document.createElement("li");
    listItem.className = "playlist-item";

    var playlistTitle = document.createElement("h3");
    playlistTitle.textContent = "El puntaje de tu playlist '" + playlist_name + "' es de: " + average_popularity;

    var progressBarContainer = document.createElement("div");
    progressBarContainer.className = "progress-bar-container";

    var progressBar = document.createElement("div");
    progressBar.className = "progress-bar";
    progressBar.style.width = average_popularity + "%";

    var comentarioDiv = document.createElement("div");
    comentarioDiv.className = "comentario-div";

    var spotifyLogo = document.createElement("img");
    spotifyLogo.setAttribute("src", "https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg");
    spotifyLogo.className = "spotify-logo";

    var comentarioLink = document.createElement("a");
    comentarioLink.setAttribute("href", playlist_url);
    comentarioLink.textContent = Comentario;
    comentarioLink.className = "comentario";

    progressBarContainer.appendChild(progressBar);
    comentarioDiv.appendChild(spotifyLogo);
    comentarioDiv.appendChild(comentarioLink);

    listItem.appendChild(playlistTitle);
    listItem.appendChild(progressBarContainer);
    listItem.appendChild(comentarioDiv);

    list.appendChild(listItem);
  }

  playlistContainer.appendChild(list);
});