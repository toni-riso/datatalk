document.addEventListener(
    "DOMContentLoaded",
    initApp
);

function initApp(){
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