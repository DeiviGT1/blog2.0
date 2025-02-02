// app/static/js/dashboard/charts_update.js

// Main function to update the charts
async function updateCharts() {
  // Get a reference to the modal
  const modal = document.getElementById('modal_update_charts');

  try {
    // Show the modal before starting the loading process
    modal.classList.add('active');

    // 1) Read values from the DOM
    const countryBar = document.getElementById("country_bar").value;
    const countryRank = document.getElementById("country_rank").value;
    const violinCheck = document.getElementById("violin_check").checked;
    const heatmapCheck = document.getElementById("heatmap_check").checked;

    // Get an array of selected team checkbox values
    const teamCheckboxes = document.querySelectorAll('input[name="teams_select"]:checked');
    const selectedTeams = Array.from(teamCheckboxes).map(cb => cb.value);
    const numTeams = document.getElementById("num_teams").value;

    // 2) Prepare the payload
    const payload = {
      country_bar: countryBar,
      country_rank: countryRank,
      show_violin: violinCheck,
      show_heatmap: heatmapCheck,
      teams: selectedTeams,
      num_teams: numTeams,
    };

    // 3) Make a POST request to /update_charts
    const resp = await fetch("/update_charts", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (!resp.ok) throw new Error("HTTP Error " + resp.status);
    const data = await resp.json();
    console.log("Received data:", data);

    // 4) Update each section (images and visibility)
    // TREND
    const trendContainer = document.getElementById("trend-chart-container");
    const trendImg = document.getElementById("trend_chart_img");
    const trendTitle = document.getElementById("trend-chart-title");
    if (data.trend_chart && trendContainer && trendImg) {
      trendContainer.style.display = "block";
      trendImg.src = "data:image/png;base64," + data.trend_chart;
      // Update title
      if (selectedTeams.length > 0) {
        trendTitle.textContent = "ELO Trend - " + selectedTeams.join(", ");
      } else {
        trendTitle.textContent = "ELO Trend";
      }
    } else if (trendContainer && trendImg) {
      trendContainer.style.display = "none";
      trendImg.src = "";
    }

    // BAR CHART
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

    // VIOLIN PLOT
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

    // Adjust data-* attributes for AI on "Team Trend"
    const trendBtn = document.querySelector("#team-trend-conclusions .ai-btn");
    if (trendBtn) {
      if (selectedTeams.length === 1) {
        trendBtn.setAttribute("data-team-trend", selectedTeams[0]);
      } else if (selectedTeams.length > 1) {
        // Adjust for multiple teams
        trendBtn.setAttribute("data-team-trend", selectedTeams.join(", "));
      } else {
        trendBtn.setAttribute("data-team-trend", "");
      }
    }

    // Adjust data-* attributes for AI on "Bar Chart"
    const barBtn = document.querySelector("#bar-chart-conclusions .ai-btn");
    if (barBtn) {
      barBtn.setAttribute("data-country-bar", countryBar);
      barBtn.setAttribute("data-country-rank", countryRank);
      barBtn.setAttribute("data-show-violin", violinCheck ? "on" : "");
      barBtn.setAttribute("data-show-heatmap", heatmapCheck ? "on" : "");
    }

    // Adjust data-* attributes for AI on "Ranking Chart"
    const rankBtn = document.querySelector("#ranking-chart-conclusions .ai-btn");
    if (rankBtn) {
      rankBtn.setAttribute("data-country-bar", countryBar);
      rankBtn.setAttribute("data-country-rank", countryRank);
      rankBtn.setAttribute("data-show-violin", violinCheck ? "on" : "");
      rankBtn.setAttribute("data-show-heatmap", heatmapCheck ? "on" : "");
    }

    // Adjust data-* attributes for AI on "Violin Plot"
    const violinBtn = document.querySelector("#violin-conclusions .ai-btn");
    if (violinBtn) {
      violinBtn.setAttribute("data-country-bar", countryBar);
      violinBtn.setAttribute("data-country-rank", countryRank);
      violinBtn.setAttribute("data-show-violin", violinCheck ? "on" : "");
      violinBtn.setAttribute("data-show-heatmap", heatmapCheck ? "on" : "");
    }

    // Adjust data-* attributes for AI on "Heatmap"
    const heatmapBtn = document.querySelector("#heatmap-conclusions .ai-btn");
    if (heatmapBtn) {
      heatmapBtn.setAttribute("data-country-bar", countryBar);
      heatmapBtn.setAttribute("data-country-rank", countryRank);
      heatmapBtn.setAttribute("data-show-violin", violinCheck ? "on" : "");
      heatmapBtn.setAttribute("data-show-heatmap", heatmapCheck ? "on" : "");
    }

  } catch (err) {
    console.error("Error updating charts:", err);
    // Optionally: show an error message to the user
    alert("An error occurred while updating charts. Please try again.");
  } finally {
    // Hide the modal after loading completes or in case of an error
    modal.classList.remove('active');
  }
}

// Listeners to update charts when any select/checkbox changes
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

  // Add listener to the "Clear selection" button to update charts after clearing selection
  if (clearTeamsBtn) {
    clearTeamsBtn.addEventListener("click", function() {
      // It is assumed that the code to clear the selection is already executed (e.g., via another inline listener or here)
      // Wait a short moment to allow checkboxes to update, then call updateCharts
      setTimeout(updateCharts, 0);
    });
  }

  // Call initially to update charts on page load
  updateCharts();
});