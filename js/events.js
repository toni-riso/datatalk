// events.js

let eventCounter = 1;

function registerEvent(eventType) {
    // Para eventos de jugador es obligatorio
    // tener un jugador seleccionado
    const eventsWithoutPlayer = [
        "goal_rival"
    ];
    if (
        !state.selectedPlayer &&
        !eventsWithoutPlayer.includes(eventType)
    ) {
        alert("Selecciona un jugador");
        return;
    }
    const event = buildEvent(eventType);
    state.events.push(event);
    registerEventOnPlayer(event);
    processSpecialEvents(event);
    addTimelineEvent(event);
    console.log("Evento registrado:", event);
    
    renderPlayerStats();
    renderTeamStats();

    saveState();
}

function buildEvent(eventType) {

    const minute =
        Math.floor(state.currentSecond / 60);

    const second =
        state.currentSecond % 60;

    return {
        id: eventCounter++,
        timestamp: new Date().toISOString(),
        matchSecond: state.currentSecond,
        minute: minute,
        second: second,
        team: state.activeTeam,
        playerId: state.selectedPlayer
            ? state.selectedPlayer.id
            : null,
        dorsal: state.selectedPlayer
            ? state.selectedPlayer.dorsal
            : null,
        playerName: state.selectedPlayer
            ? state.selectedPlayer.name
            : null,
        position: state.selectedPlayer
            ? state.selectedPlayer.position
            : null,
        eventType: eventType
    };

}

function registerEventOnPlayer(event) {
    if (!event.playerId) {
        return;
    }
    const player =
        state.players.find(
            p => p.id === event.playerId
        );
    if (!player) {
        return;
    }
    player.events.push(event);
}

function processSpecialEvents(event) {
    switch(event.eventType){
        case "goal_own":
            state.homeGoals++;
            updateScoreBoard();
            break;
        case "goal_rival":
            state.awayGoals++;
            updateScoreBoard();
            break;
        case "yellow":
            updateYellowCards(
                event.playerId
            );
            break;
    }
}

function updateYellowCards(playerId){
    const player =
        state.players.find(
            p => p.id === playerId
        );
    if(!player) return;
    player.yellowCards++;
}

function eventLabel(eventType){
    const labels = {
        pass_ok:
            "✅ Pase bien",
        pass_bad:
            "❌ Pase mal",
        dribble_ok:
            "✅ Regate bien",
        dribble_bad:
            "❌ Regate mal",
        shot:
            "🎯 Tiro",
        shot_target:
            "🥅 A puerta",
        goal_own:
            "⚽ Gol nuestro",
        goal_rival:
            "⚽ Gol rival",
        loss:
            "💥 Pérdida",
        recovery:
            "🔁 Recuperación",
        foul_committed:
            "🤕 Falta cometida",
        foul_received:
            "🙋 Falta sufrida",
        yellow:
            "🟨 Amarilla",
        substitution:
            "🔄 Cambio"
    };
    return labels[eventType] || eventType;
}

function registerSubstitutionEvent(
    playerOut,
    playerIn
) {
    const event = {
        id:
            Date.now(),
        minute:
            getCurrentMinute(),
        team:
            "home",
        eventType:
            "substitution",
        playerOut:
            playerOut.id,
        playerIn:
            playerIn.id,
        description:
            `${playerOut.dorsal} → ${playerIn.dorsal}`
    };
    state.events.push(
        event
    );
    addTimelineEvent(event);
}

function initializeUndoButton() {
    const button =
        document.getElementById(
            "undoEventBtn"
        );
    if (!button) {
        return;
    }
    button.addEventListener(
        "click",
        undoLastEvent
    );
}

function undoLastEvent() {
    if (
        state.events.length === 0
    ) {
        alert(
            "No hay eventos para deshacer."
        );
        return;
    }
    const lastEvent =
        state.events.pop();
    revertEventEffects(
        lastEvent
    );
    renderTimeline();
    console.log(
        "Evento eliminado:",
        lastEvent
    );

    renderPlayerStats();
    renderTeamStats();
    
    saveState();

}

function revertEventEffects(event) {
    switch (
        event.eventType
    ) {
        case "goal_own":
            state.homeGoals--;
            if (
                state.homeGoals < 0
            ) {
                state.homeGoals = 0;
            }
            updateScoreBoard();
            break;
        case "goal_rival":
            state.awayGoals--;
            if (
                state.awayGoals < 0
            ) {
                state.awayGoals = 0;
            }
            updateScoreBoard();
            break;
        case "yellow":
            const player =
                state.players.find(
                    p =>
                    p.id ===
                    event.playerId
                );
            if (
                player &&
                player.yellowCards > 0
            ) {

                player.yellowCards--;
            }
            break;
        case "substitution":
            undoSubstitution(event);
            break;
    }
}

function undoSubstitution(event) {
    const playerOut =
        state.players.find(
            p =>
            p.id ===
            event.playerOutId
        );
    const playerIn =
        state.players.find(
            p =>
            p.id ===
            event.playerInId
        );
    if (
        !playerOut ||
        !playerIn
    ) {
        return;
    }
    playerOut.active = true;
    playerOut.exitMinute = null;
    playerIn.active = false;
    playerIn.entryMinute = null;
    renderFieldPlayers();
}
