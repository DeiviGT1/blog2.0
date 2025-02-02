// app/static/js/dashboard/charts_update.js

// Función principal para actualizar los gráficos
async function updateCharts() {
  // Obtener referencia al modal
  const modal = document.getElementById('modal_update_charts');

  try {
    // Mostrar el modal antes de iniciar la carga
    modal.classList.add('active');

    // 1) Leer valores del DOM
    const countryBar = document.getElementById("country_bar").value;
    const countryRank = document.getElementById("country_rank").value;
    const violinCheck = document.getElementById("violin_check").checked;
    const heatmapCheck = document.getElementById("heatmap_check").checked;

    // Obtener un array de valores seleccionados de los checkboxes de equipos
    const teamCheckboxes = document.querySelectorAll('input[name="teams_select"]:checked');
    const selectedTeams = Array.from(teamCheckboxes).map(cb => cb.value);
    const numTeams = document.getElementById("num_teams").value;

    // 2) Preparar payload
    const payload = {
      country_bar: countryBar,
      country_rank: countryRank,
      show_violin: violinCheck,
      show_heatmap: heatmapCheck,
      teams: selectedTeams,
      num_teams: numTeams,
    };

    // 3) Hacer POST a /update_charts
    const resp = await fetch("/update_charts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (!resp.ok) throw new Error("Error HTTP " + resp.status);
    const data = await resp.json();
    console.log("Datos recibidos:", data);

    // 4) Actualizar cada sección (imágenes y visibilidad)
    // TENDENCIA
    const trendContainer = document.getElementById("trend-chart-container");
    const trendImg = document.getElementById("trend_chart_img");
    const trendTitle = document.getElementById("trend-chart-title");
    if (data.trend_chart && trendContainer && trendImg) {
      trendContainer.style.display = "block";
      trendImg.src = "data:image/png;base64," + data.trend_chart;
      // Actualiza título
      if (selectedTeams.length > 0) {
        trendTitle.textContent = "Tendencia del ELO - " + selectedTeams.join(", ");
      } else {
        trendTitle.textContent = "Tendencia del ELO";
      }
    } else if (trendContainer && trendImg) {
      trendContainer.style.display = "none";
      trendImg.src = "";
    }

    // BAR
    const barContainer = document.getElementById("bar-chart-container");
    const barImg = document.getElementById("bar_chart_img");
    if (data.bar_chart && barContainer && barImg) {
      barContainer.style.display = "block";
      barImg.src = "data:image/png;base64," + data.bar_chart;
    } else if (barContainer && barImg) {
      barContainer.style.display = "none";
      barImg.src = "";
    }

    // RANKING
    const rankContainer = document.getElementById("ranking-chart-container");
    const rankImg = document.getElementById("rank_chart_img");
    if (data.rank_chart && rankContainer && rankImg) {
      rankContainer.style.display = "block";
      rankImg.src = "data:image/png;base64," + data.rank_chart;
    } else if (rankContainer && rankImg) {
      rankContainer.style.display = "none";
      rankImg.src = "";
    }

    // VIOLIN
    const violinContainer = document.getElementById("violin-chart-container");
    const violinImg = document.getElementById("violin_chart_img");
    if (data.violin_chart && violinContainer && violinImg) {
      violinContainer.style.display = "block";
      violinImg.src = "data:image/png;base64," + data.violin_chart;
    } else if (violinContainer && violinImg) {
      violinContainer.style.display = "none";
      violinImg.src = "";
    }

    // HEATMAP
    const heatmapContainer = document.getElementById("heatmap-chart-container");
    const heatmapImg = document.getElementById("heatmap_chart_img");
    if (data.heatmap_chart && heatmapContainer && heatmapImg) {
      heatmapContainer.style.display = "block";
      heatmapImg.src = "data:image/png;base64," + data.heatmap_chart;
    } else if (heatmapContainer && heatmapImg) {
      heatmapContainer.style.display = "none";
      heatmapImg.src = "";
    }

    // Ajustar data-* de IA para "Team Trend"
    const trendBtn = document.querySelector("#team-trend-conclusions .ai-btn");
    if (trendBtn) {
      if (selectedTeams.length === 1) {
        trendBtn.setAttribute("data-team-trend", selectedTeams[0]);
      } else if (selectedTeams.length > 1) {
        // Ajustar para varios equipos
        trendBtn.setAttribute("data-team-trend", selectedTeams.join(", "));
      } else {
        trendBtn.setAttribute("data-team-trend", "");
      }
    }

    // Ajustar data-* de IA para "Bar Chart"
    const barBtn = document.querySelector("#bar-chart-conclusions .ai-btn");
    if (barBtn) {
      barBtn.setAttribute("data-country-bar", countryBar);
      barBtn.setAttribute("data-country-rank", countryRank);
      barBtn.setAttribute("data-show-violin", violinCheck ? "on" : "");
      barBtn.setAttribute("data-show-heatmap", heatmapCheck ? "on" : "");
    }

    // Ajustar data-* de IA para "Ranking Chart"
    const rankBtn = document.querySelector("#ranking-chart-conclusions .ai-btn");
    if (rankBtn) {
      rankBtn.setAttribute("data-country-bar", countryBar);
      rankBtn.setAttribute("data-country-rank", countryRank);
      rankBtn.setAttribute("data-show-violin", violinCheck ? "on" : "");
      rankBtn.setAttribute("data-show-heatmap", heatmapCheck ? "on" : "");
    }

    // Ajustar data-* de IA para "Violin Plot"
    const violinBtn = document.querySelector("#violin-conclusions .ai-btn");
    if (violinBtn) {
      violinBtn.setAttribute("data-country-bar", countryBar);
      violinBtn.setAttribute("data-country-rank", countryRank);
      violinBtn.setAttribute("data-show-violin", violinCheck ? "on" : "");
      violinBtn.setAttribute("data-show-heatmap", heatmapCheck ? "on" : "");
    }

    // Ajustar data-* de IA para "Heatmap"
    const heatmapBtn = document.querySelector("#heatmap-conclusions .ai-btn");
    if (heatmapBtn) {
      heatmapBtn.setAttribute("data-country-bar", countryBar);
      heatmapBtn.setAttribute("data-country-rank", countryRank);
      heatmapBtn.setAttribute("data-show-violin", violinCheck ? "on" : "");
      heatmapBtn.setAttribute("data-show-heatmap", heatmapCheck ? "on" : "");
    }

  } catch (err) {
    console.error("Error al actualizar gráficos:", err);
    // Opcional: mostrar un mensaje de error al usuario
    alert("Ocurrió un error al actualizar los gráficos. Por favor, intenta nuevamente.");
  } finally {
    // Ocultar el modal después de que la carga haya finalizado o en caso de error
    modal.classList.remove('active');
  }
}

// Listeners para que cada vez que cambie un select/checkbox, se actualicen gráficas
document.addEventListener("DOMContentLoaded", function() {
  const countryBarSelect = document.getElementById("country_bar");
  const countryRankSelect = document.getElementById("country_rank");
  const violinCheck = document.getElementById("violin_check");
  const heatmapCheck = document.getElementById("heatmap_check");
  const teamsCheckboxContainer = document.getElementById("teams-checkbox-container");
  const numTeams = document.getElementById("num_teams");
  const clearTeamsBtn = document.getElementById("clear-teams");

  if (countryBarSelect) countryBarSelect.addEventListener("change", updateCharts);
  if (countryRankSelect) countryRankSelect.addEventListener("change", updateCharts);
  if (violinCheck) violinCheck.addEventListener("change", updateCharts);
  if (heatmapCheck) heatmapCheck.addEventListener("change", updateCharts);
  if (teamsCheckboxContainer) teamsCheckboxContainer.addEventListener("change", updateCharts);
  if (numTeams) numTeams.addEventListener("change", updateCharts);

  // Agregar listener al botón "Quitar selección" para actualizar gráficos tras borrar la selección
  if (clearTeamsBtn) {
    clearTeamsBtn.addEventListener("click", function() {
      // Se asume que el código que limpia la selección ya se ejecuta (por ejemplo, mediante otro listener inline o aquí mismo)
      // Esperamos un corto lapso para que los checkboxes se actualicen y luego llamamos a updateCharts
      setTimeout(updateCharts, 0);
    });
  }

  // Llamar al inicio para actualizar
  updateCharts();
});