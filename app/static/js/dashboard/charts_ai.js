document.addEventListener("DOMContentLoaded", function () {
  document.addEventListener("click", async function (e) {
    if (e.target && e.target.classList.contains("ai-btn")) {
      e.preventDefault();

      const btn = e.target;
      const chartType = btn.getAttribute("data-chart-type") || "";
      const countryBar = btn.getAttribute("data-country-bar") || "";
      const countryRank = btn.getAttribute("data-country-rank") || "";
      const teamTrend = btn.getAttribute("data-team-trend") || "";
      const showViolin = btn.getAttribute("data-show-violin") === "on";
      const showHeatmap = btn.getAttribute("data-show-heatmap") === "on";

      const payload = {
        chart_type: chartType,
        country_bar: countryBar,
        country_rank: countryRank,
        team_trend: teamTrend,
        show_violin: showViolin,
        show_heatmap: showHeatmap,
      };

      try {
        const response = await fetch("/generate_conclusions_ajax", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload),
        });
        if (!response.ok) {
          throw new Error(`Error HTTP: ${response.status}`);
        }
        const data = await response.json();
        const text = data.conclusions || "Sin conclusiones";

        let divId = "";
        if (chartType === "bar_chart") divId = "bar-chart-conclusions";
        if (chartType === "ranking_chart") divId = "ranking-chart-conclusions";
        if (chartType === "violin_plot") divId = "violin-conclusions";
        if (chartType === "heatmap") divId = "heatmap-conclusions";
        if (chartType === "team_trend_chart") divId = "team-trend-conclusions";

        if (divId) {
          const conclusionsDiv = document.getElementById(divId);
          if (conclusionsDiv) {
            conclusionsDiv.innerHTML = `
                  <button class="ai-btn"
                          data-chart-type="${chartType}"
                          data-country-bar="${countryBar}"
                          data-country-rank="${countryRank}"
                          data-team-trend="${teamTrend}"
                          data-show-violin="${showViolin ? "on" : ""}"
                          data-show-heatmap="${showHeatmap ? "on" : ""}">
                    Conclusiones IA (${chartType})
                  </button>
                  <h3>Conclusiones IA:</h3>
                  <div>${text}</div>
                `;
          }
        }
      } catch (err) {
        console.error("Error generando conclusiones con IA:", err);
      }
    }
  });
});
