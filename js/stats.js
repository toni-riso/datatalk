//stats.js
function calculatePlayerStats(playerId) {
    const stats = {
        pass_ok: 0,
        pass_bad: 0,
        dribble_ok: 0,
        dribble_bad: 0,
        shot: 0,
        shot_target: 0,
        goal_own: 0,
        recovery: 0,
        loss: 0,
        foul_committed: 0,
        foul_received: 0,
        yellow: 0
    };
    state.events.forEach(event => {
        if (
            event.playerId !== playerId
        ) {
            return;
        }
        if (
            stats[event.eventType] !==
            undefined
        ) {
            stats[event.eventType]++;
        }
    });
    return stats;
}

function renderPlayerStats() {
    const container =
        document.getElementById(
            "playerStats"
        );
    if (!container) {
        return;
    }

    if (!state.selectedPlayer) {
        container.innerHTML = `
            <div class="stats-empty">
                Selecciona un jugador
            </div>
        `;
        return;
    }
    const stats =
        calculatePlayerStats(
            state.selectedPlayer.id
        );
    
    const passPercentage =
        calculatePercentage(
            stats.pass_ok,
            stats.pass_bad
        );
    
    const dribblePercentage =
        calculatePercentage(
            stats.dribble_ok,
            stats.dribble_bad
        );
    
    const minutesPlayed =
        calculateMinutesPlayed(
            state.selectedPlayer
        );
    
    const rating =
        calculatePlayerRating(
            state.selectedPlayer.id
        );
    
    container.innerHTML = `
        <div class="player-stats-header">
            <h3>
                ${state.selectedPlayer.dorsal} -
                ${state.selectedPlayer.name}
            </h3>
            <p>
                ${state.selectedPlayer.position}
            </p>
            <div class="player-summary">
                <span class="minutes-played">
                    ⏱ ${minutesPlayed} min
                </span>
                <span class="player-rating">
                    ⭐ ${rating}
                </span>
            </div>
        </div>

        <div class="stats-grid">
            <div class="stat-box">
                <span class="stat-label">
                    ✅ Pase bien
                </span>
                <span class="stat-value">
                    ${stats.pass_ok}
                </span>
            </div>
            <div class="stat-box">
                <span class="stat-label">
                    ❌ Pase mal
                </span>
                <span class="stat-value">
                    ${stats.pass_bad}
                </span>
            </div>
            <div class="stat-box">
                <span class="stat-label">
                📈 % Pase
                </span>
                <span class="stat-value">
                    ${passPercentage}%
                </span>
            </div>
            <div class="stat-box">
                <span class="stat-label">
                    ✅ Regate bien
                </span>
                <span class="stat-value">
                    ${stats.dribble_ok}
                </span>
            </div>
            <div class="stat-box">
                <span class="stat-label">
                    ❌ Regate mal
                </span>
                <span class="stat-value">
                    ${stats.dribble_bad}
                </span>
            </div>
            <div class="stat-box">
                <span class="stat-label">
                📈 % Regate
                </span>
                <span class="stat-value">
                    ${dribblePercentage}
                </span>
            </div>

            <div class="stat-box">
                <span class="stat-label">
                    🎯 Tiros
                </span>
                <span class="stat-value">
                    ${stats.shot}
                </span>
            </div>
            <div class="stat-box">
                <span class="stat-label">
                    🥅 A puerta
                </span>
                <span class="stat-value">
                    ${stats.shot_target}
                </span>
            </div>
            <div class="stat-box">
                <span class="stat-label">
                    ⚽ Goles
                </span>
                <span class="stat-value">
                    ${stats.goal_own}
                </span>
            </div>
            <div class="stat-box">
                <span class="stat-label">
                    🔁 Recuperaciones
                </span>
                <span class="stat-value">
                    ${stats.recovery}
                </span>
            </div>
            <div class="stat-box">
                <span class="stat-label">
                    💥 Pérdidas
                </span>
                <span class="stat-value">
                    ${stats.loss}
                </span>
            </div>
            <div class="stat-box">
                <span class="stat-label">
                    🤕 F. cometidas
                </span>
                <span class="stat-value">
                    ${stats.foul_committed}
                </span>
            </div>
            <div class="stat-box">
                <span class="stat-label">
                    🙋 F. sufridas
                </span>
                <span class="stat-value">
                    ${stats.foul_received}
                </span>
            </div>
            <div class="stat-box">
                <span class="stat-label">
                    🟨 Amarillas
                </span>
                <span class="stat-value">
                    ${stats.yellow}
                </span>
            </div>
        </div>
    `;
}

function calculateMinutesPlayed(
    player
) {
    let minutes = 0;
    player.stints.forEach(stint => {
        const start =
            stint.in;
        const end =
            stint.out === null
                ? getCurrentMinute()
                : stint.out;
        minutes +=
            end - start;
    });
    return minutes;
}

function calculatePercentage(
    success,
    fail
) {
    const total =
        success + fail;
    if (total === 0) {
        return 0;
    }
    return Math.round(
        (success / total) * 100
    );
}

function calculateTeamStats() {
    const stats = {
        pass_ok: 0,
        pass_bad: 0,
        dribble_ok: 0,
        dribble_bad: 0,
        shot: 0,
        shot_target: 0,
        goal_own: 0,
        recovery: 0,
        loss: 0,
        foul_committed: 0,
        foul_received: 0,
        yellow: 0
    };
    state.events.forEach(event => {
        if (event.team !== "home") {
            return;
        }
        if (
            stats[event.eventType] !==
            undefined
        ) {
            stats[event.eventType]++;
        }
    });
    return stats;
}

function renderTeamStats() {
    const container =
        document.getElementById(
            "teamStats"
        );
    if (!container) {
        return;
    }
    const stats =
        calculateTeamStats();
    const passPercentage =
        calculatePercentage(
            stats.pass_ok,
            stats.pass_bad
        );
    const dribblePercentage =
        calculatePercentage(
            stats.dribble_ok,
            stats.dribble_bad
        );
    container.innerHTML = `
        <div class="stats-grid">
            <div class="stat-box">
                <span class="stat-label">
                    ✅ Pase bien
                </span>
                <span class="stat-value">
                    ${stats.pass_ok}
                </span>
            </div>
            <div class="stat-box">
                <span class="stat-label">
                    ❌ Pase mal
                </span>
                <span class="stat-value">
                    ${stats.pass_bad}
                </span>
            </div>
            <div class="stat-box">
                <span class="stat-label">
                    📈 % Pase
                </span>
                <span class="stat-value">
                    ${passPercentage}%
                </span>
            </div>
            <div class="stat-box">
                <span class="stat-label">
                    ✅ Regate bien
                </span>
                <span class="stat-value">
                    ${stats.dribble_ok}
                </span>
            </div>
            <div class="stat-box">
                <span class="stat-label">
                    ❌ Regate mal
                </span>
                <span class="stat-value">
                    ${stats.dribble_bad}
                </span>
            </div>
            <div class="stat-box">
                <span class="stat-label">
                    📈 % Regate
                </span>
                <span class="stat-value">
                    ${dribblePercentage}%
                </span>
            </div>
            <div class="stat-box">
                <span class="stat-label">
                    🎯 Tiros
                </span>
                <span class="stat-value">
                    ${stats.shot}
                </span>
            </div>
            <div class="stat-box">
                <span class="stat-label">
                    🥅 A puerta
                </span>
                <span class="stat-value">
                    ${stats.shot_target}
                </span>
            </div>
            <div class="stat-box">
                <span class="stat-label">
                    ⚽ Goles
                </span>
                <span class="stat-value">
                    ${stats.goal_own}
                </span>
            </div>
            <div class="stat-box">
                <span class="stat-label">
                    🔁 Recuperaciones
                </span>
                <span class="stat-value">
                    ${stats.recovery}
                </span>
            </div>
            <div class="stat-box">
                <span class="stat-label">
                    💥 Pérdidas
                </span>
                <span class="stat-value">
                    ${stats.loss}
                </span>
            </div>
            <div class="stat-box">
                <span class="stat-label">
                    🤕 F. cometidas
                </span>
                <span class="stat-value">
                    ${stats.foul_committed}
                </span>
            </div>
            <div class="stat-box">
                <span class="stat-label">
                    🙋 F. sufridas
                </span>
                <span class="stat-value">
                    ${stats.foul_received}
                </span>
            </div>
            <div class="stat-box">
                <span class="stat-label">
                    🟨 Amarillas
                </span>
                <span class="stat-value">
                    ${stats.yellow}
                </span>
            </div>
        </div>
    `;
}

function calculatePlayerRating(
    playerId
) {
    const stats =
        calculatePlayerStats(
            playerId
        );
    let rating = 5;
    rating += stats.pass_ok * 0.1;
    rating -= stats.pass_bad * 0.1;
    rating += stats.dribble_ok * 0.3;
    rating -= stats.dribble_bad * 0.3;
    rating += stats.shot * 0.2;
    rating += stats.shot_target * 0.4;
    rating += stats.goal_own * 2;
    rating += stats.recovery * 0.3;
    rating -= stats.loss * 0.3;
    rating -= stats.foul_committed * 0.2;
    rating += stats.foul_received * 0.2;
    rating -= stats.yellow * 1;
    rating =
        Math.max(
            0,
            Math.min(10, rating)
        );
    return rating.toFixed(1);
}