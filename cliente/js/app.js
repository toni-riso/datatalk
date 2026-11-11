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
    initializeVenueSetting();
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

function initializeVenueSetting() {
    const venue =
        document.getElementById("venue");
    if (!venue) {
        return;
    }

    if (
        state.matchData.venue === "home" ||
        state.matchData.venue === "away"
    ) {
        venue.value = state.matchData.venue;
    } else {
        state.matchData.venue = venue.value;
    }

    venue.addEventListener("change", () => {
        state.matchData.venue = venue.value;
        saveState();
    });
}

if (
    "serviceWorker"
    in navigator
) {
    window.addEventListener(
        "load",
        () => {
            navigator
                .serviceWorker
                .register(
                    "./service-worker.js"
                )
                .then(() => {
                    console.log(
                        "Service Worker registrado"
                    );
                })
                .catch(error => {
                    console.error(
                        error
                    );
                });
        }
    );
}