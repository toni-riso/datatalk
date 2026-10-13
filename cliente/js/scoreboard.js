function updateScoreBoard(){
    document.getElementById("homeGoals").textContent =
        state.homeGoals;
    document.getElementById("awayGoals").textContent =
        state.awayGoals;
    document.getElementById("stickyHomeGoals").textContent =
        state.homeGoals;
    document.getElementById("stickyAwayGoals").textContent =
        state.awayGoals;
}