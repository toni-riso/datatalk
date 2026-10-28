// events.js

let eventCounter = 1;

function registerEvent(eventType) {
    // Para eventos de jugador es obligatorio
    // tener un jugador seleccionado
    const eventsWithoutPlayer = [
        "buildout_success",
        "buildout_fail",
        "rival_buildout_success",
        "rival_buildout_fail",
        "rival_shot_off",
        "rival_shot_target",
        "goal_rival"    
    ];
    
    const playerRequired =
    !eventsWithoutPlayer.includes(
        eventType
    );

    if (playerRequired && !state.selectedPlayer) {
        alert("Selecciona un jugador");
        return;
    }   
    const event = buildEvent(eventType);
    state.events.push(event);

    processSpecialEvents(event);
    addTimelineEvent(event);
    console.log("Evento registrado:", event);
    
    renderPlayerStats();
    renderTeamStats();

    saveState();
}

function buildEvent(eventType) {

    const minute =Math.floor(state.currentSecond / 60);

    const second =state.currentSecond % 60;

    const eventsWithoutPlayer = [

        "buildout_success",
        "buildout_fail",

        "rival_buildout_success",
        "rival_buildout_fail",

        "rival_shot_off",
        "rival_shot_target",

        "goal_rival"

    ];

    const requiresPlayer =!eventsWithoutPlayer.includes(eventType);

    return {
        id: eventCounter++,
        timestamp:new Date().toISOString(),
        matchSecond:state.currentSecond,
        minute:minute,
        second:second,
        team:state.activeTeam,

        playerId:
            requiresPlayer
                ? state.selectedPlayer?.id
                : null,
        dorsal:
            requiresPlayer
                ? state.selectedPlayer?.dorsal
                : null,
        playerName:
            requiresPlayer
                ? state.selectedPlayer?.name
                : null,
        position:
            requiresPlayer
                ? state.selectedPlayer?.position
                : null,
        eventType:
            eventType
    };
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

function eventLabel(
    eventType
) {
    const labels = {
        buildout_success:
            "✅ Salida exitosa",
        buildout_fail:
            "❌ Salida fallida",
        rival_buildout_success:
            "✅ Rival salida exitosa",
        rival_buildout_fail:
            "❌ Rival salida fallida",
        loss_buildout:
            "❌ Pérdida salida",
        dribble_ok:
            "✅ Regate",
        dribble_bad:
            "❌ Regate",
        loss_build:
            "❌ Pérdida construcción",
        shot_off:
            "🎯 Tiro fuera",
        shot_target:
            "🥅 Tiro a puerta",
        rival_shot_off:
            "🎯 Rival tiro fuera",
        rival_shot_target:
            "🥅 Rival tiro a puerta",
        loss_finish:
            "❌ Pérdida finalización",
        goal_own:
            "⚽ Gol",
        goal_rival:
            "⚽ Gol rival",
        recovery_buildout:
            "🔁 Recuperación salida",
        recovery_build:
            "🔁 Recuperación construcción",
        recovery_finish:
            "🔁 Recuperación finalización",
        foul_committed:
            "🤕 Falta cometida",
        foul_received:
            "🙋 Falta sufrida",
        yellow:
            "🟨 Amarilla",
        substitution:
            "🔄 Cambio"
    };
    return (
        labels[eventType] ||
        eventType
    );
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
