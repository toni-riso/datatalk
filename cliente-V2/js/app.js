document.addEventListener(
    "DOMContentLoaded",
    initApp
);

function initApp(){
    loadState();
    initializePlayers();
    renderSquad();
    renderFieldPlayers();
    updateTimerDisplay();
    updateScoreBoard();
    initializeEvents();
    initializeTimer();
    initializeCollapsibles();
    initializeLineupButton();
    initializeSubstitutions();
    initializeUndoButton();
    initializeNewMatchButton();
    renderTeamStats();
    initializeMatchSettings();
    initializeExportButton();
}

function initializeEvents(){
    const buttons = document.querySelectorAll("[data-event]");
    buttons.forEach(button => {
        button.addEventListener(
            "click",
            () => {
                registerEvent(
                    button.dataset.event
                );
            }
        );
    });
}

function initializeLineupButton() {
    const button =
        document.getElementById(
            "confirmLineupBtn"
        );
    if (!button) return;
    button.addEventListener(
        "click",
        () => {
            collapseMatchAndSquad();
        }
    );
}

function initializeNewMatchButton() {
    const newMatchBtn =
        document.getElementById(
            "newMatchBtn"
        );
    if (!newMatchBtn) {
        return;
    }
    newMatchBtn.addEventListener(
        "click",
        newMatch
    );
}

function initializeMatchSettings() {
    const matchType =
        document.getElementById(
            "matchType"
        );
    if (!matchType) {
        return;
    }
    matchType.value =
        state.matchType;
    matchType.addEventListener(
        "change",
        () => {
            state.matchType =
                matchType.value;
            state.playersOnField =
                state.matchType === "F11"
                    ? 11
                    : 8;
            saveState();
        }
    );
}

