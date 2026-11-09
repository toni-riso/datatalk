//stats.js
function calculatePlayerStats(playerId) {
    const stats = {
        loss_buildout: 0,
        dribble_ok: 0,
        dribble_bad: 0,
        loss_build: 0,
        shot_off: 0,
        shot_target: 0,
        loss_finish: 0,
        goal_own: 0,
        assist: 0,
        recovery_buildout: 0,
        recovery_build: 0,
        recovery_finish: 0,
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
    
    const minutesPlayed =
        calculateMinutesPlayed(
            state.selectedPlayer
        );
    
        container.innerHTML = `

        <div class="player-stats-header">
            <h3>
                ${state.selectedPlayer.dorsal} - ${state.selectedPlayer.name}
            </h3>
    
            <p class="player-position">${state.selectedPlayer.position}</p>

            <div class="player-summary">
                <span class="minutes-played"> ⏱ ${minutesPlayed} min </span>
            </div>
        </div>
        <div class="team-stats-section section-salida">
                <h3>⚙️ Salida balón</h3>
    
            <div class="stats-grid">
    
                <div class="stat-box">
                    <span class="stat-label">
                        ❌ Pérdidas salida
                    </span>
                    <span class="stat-value">
                        ${stats.loss_buildout}
                    </span>
                </div>
    
            </div>    
        </div>

          

        <div class="team-stats-section section-construccion">
        <h3>⚙️ Construcción</h3>  
            <div class="stats-grid">
    
                <div class="stat-box">
                    <span class="stat-label">
                        ✅ Regates
                    </span>
                    <span class="stat-value">
                        ${stats.dribble_ok}
                    </span>
                </div>
    
                <div class="stat-box">
                    <span class="stat-label">
                        ❌ Regates
                    </span>
                    <span class="stat-value">
                        ${stats.dribble_bad}
                    </span>
                </div>
    
                <div class="stat-box">
                    <span class="stat-label">
                        ❌ Pérdidas construcción
                    </span>
                    <span class="stat-value">
                        ${stats.loss_build}
                    </span>
                </div>
    
            </div>
        </div>
    
        <div class="team-stats-section section-finalizacion">
    
            <h3>Finalización</h3>
    
            <div class="stats-grid">
    
                <div class="stat-box">
                    <span class="stat-label">
                        🎯 Tiros fuera
                    </span>
                    <span class="stat-value">
                        ${stats.shot_off}
                    </span>
                </div>
    
                <div class="stat-box">
                    <span class="stat-label">
                        🥅 Tiros a puerta
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
                        🅰️ Asistencias
                    </span>
                    <span class="stat-value">
                        ${stats.assist}
                    </span>
                </div>
    
                <div class="stat-box">
                    <span class="stat-label">
                        ❌ Pérdidas finalización
                    </span>
                    <span class="stat-value">
                        ${stats.loss_finish}
                    </span>
                </div>
    
            </div>
    
        </div>
    
        <div class="team-stats-section section-defensa">
    
            <h3>Defensa</h3>
    
            <div class="stats-grid">
    
                <div class="stat-box">
                    <span class="stat-label">
                        🔁 Rec. salida
                    </span>
                    <span class="stat-value">
                        ${stats.recovery_buildout}
                    </span>
                </div>
    
                <div class="stat-box">
                    <span class="stat-label">
                        🔁 Rec. construcción
                    </span>
                    <span class="stat-value">
                        ${stats.recovery_build}
                    </span>
                </div>
    
                <div class="stat-box">
                    <span class="stat-label">
                        🔁 Rec. finalización
                    </span>
                    <span class="stat-value">
                        ${stats.recovery_finish}
                    </span>
                </div>
    
            </div>
    
        </div>
    
        <div class="team-stats-section section-disciplina">
    
            <h3>Disciplina</h3>
    
            <div class="stats-grid">
    
                <div class="stat-box">
                    <span class="stat-label">
                        🤕 Faltas cometidas
                    </span>
                    <span class="stat-value">
                        ${stats.foul_committed}
                    </span>
                </div>
    
                <div class="stat-box">
                    <span class="stat-label">
                        🙋 Faltas sufridas
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
        buildout_success: 0,
        buildout_fail: 0,
        rival_buildout_success: 0,
        rival_buildout_fail: 0,
        loss_buildout: 0,
        dribble_ok: 0,
        dribble_bad: 0,
        loss_build: 0,
        shot_off: 0,
        shot_target: 0,
        rival_shot_off: 0,
        rival_shot_target: 0,
        loss_finish: 0,
        goal_own: 0,
        rival_goal: 0,
        assist: 0,
        corner_for: 0,
        rival_corner: 0,
        recovery_buildout: 0,
        recovery_build: 0,
        recovery_finish: 0,
        foul_committed: 0,
        foul_received: 0,
        yellow: 0
    };
    state.events.forEach(event => {
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

    const buildoutPercentage =
        calculatePercentage(
            stats.buildout_success,
            stats.buildout_fail
        );

    const pressurePercentage =
        calculatePercentage(
            stats.rival_buildout_fail,
            stats.rival_buildout_success
        );

    const dribblePercentage =
        calculatePercentage(
            stats.dribble_ok,
            stats.dribble_bad
        );

    container.innerHTML = `

        <div class="team-stats-section">
            <h3>Salida</h3>
            <div class="stats-grid">

                <div class="stat-box">
                    <span class="stat-label">✅ Salidas exitosas</span>
                    <span class="stat-value">${stats.buildout_success} </span>
                </div>

                <div class="stat-box">
                    <span class="stat-label">❌ Salidas fallidas</span>
                    <span class="stat-value">${stats.buildout_fail}</span>
                </div>
                <div class="stat-box">
                    <span class="stat-label">📈 % Salida</span>
                    <span class="stat-value">${buildoutPercentage}%</span>
                </div>
                <div class="stat-box">
                    <span class="stat-label">✅ Rival salida </span>
                    <span class="stat-value">  ${stats.rival_buildout_success}</span>
                </div>
                <div class="stat-box">
                    <span class="stat-label">❌ Rival salida</span>
                    <span class="stat-value">${stats.rival_buildout_fail}</span>
                </div>
                <div class="stat-box">
                    <span class="stat-label">📈 Presión</span>
                    <span class="stat-value">${pressurePercentage}%</span>
                </div>
            </div>
        </div>
        <div class="team-stats-section">
            <h3>Construcción</h3>
            <div class="stats-grid">
                <div class="stat-box">
                    <span class="stat-label">✅ Regates </span>
                    <span class="stat-value"> ${stats.dribble_ok}</span>
                </div>
                <div class="stat-box">
                    <span class="stat-label">❌ Regates</span>
                    <span class="stat-value">${stats.dribble_bad}</span>
                </div>
                <div class="stat-box">
                    <span class="stat-label"> 📈 % Regate</span>
                    <span class="stat-value">${dribblePercentage}% </span>
                </div>
                <div class="stat-box">
                    <span class="stat-label">❌ Pérdidas salida</span>
                    <span class="stat-value">  ${stats.loss_buildout}</span>
                </div>
                <div class="stat-box">
                    <span class="stat-label">❌ Pérdidas construcción</span>
                    <span class="stat-value"> ${stats.loss_build}</span>
                </div>
            </div>
        </div>
        <div class="team-stats-section">
            <h3>Finalización</h3>
            <div class="stats-grid">
                <div class="stat-box">
                    <span class="stat-label">🎯 Tiros fuera</span>
                    <span class="stat-value"> ${stats.shot_off} </span>
                </div>
                <div class="stat-box">
                    <span class="stat-label"> 🥅 Tiros a puerta</span>
                    <span class="stat-value"> ${stats.shot_target}</span>
                </div>
                <div class="stat-box">
                    <span class="stat-label">⚽ Goles </span>
                    <span class="stat-value">${stats.goal_own}</span>
                </div>
                <div class="stat-box">
                    <span class="stat-label"> ❌ Pérdidas finalización</span>
                    <span class="stat-value">${stats.loss_finish}</span>
                </div>
                <div class="stat-box">
                    <span class="stat-label">🎯 Rival fuera </span>
                    <span class="stat-value">${stats.rival_shot_off}</span>
                </div>
                <div class="stat-box">
                    <span class="stat-label"> 🥅 Rival puerta</span>
                    <span class="stat-value">   ${stats.rival_shot_target} </span>
                </div>
                <div class="stat-box">
                    <span class="stat-label"> ⚽ Goles rival</span>
                    <span class="stat-value">  ${stats.rival_goal}</span>
                </div>
            </div>
        </div>

        <div class="team-stats-section">
            <h3>Balón parado</h3>
            <div class="stats-grid">
                <div class="stat-box">
                    <span class="stat-label">🅰️ Asistencias</span>
                    <span class="stat-value">${stats.assist}</span>
                </div>
                <div class="stat-box">
                    <span class="stat-label">🚩 Córners a favor</span>
                    <span class="stat-value">${stats.corner_for}</span>
                </div>
                <div class="stat-box">
                    <span class="stat-label">🚩 Córners en contra</span>
                    <span class="stat-value">${stats.rival_corner}</span>
                </div>
            </div>
        </div>

        <div class="team-stats-section">
            <h3>Defensa</h3>
            <div class="stats-grid">
                <div class="stat-box">
                    <span class="stat-label">🔁 Rec. salida</span>
                    <span class="stat-value">${stats.recovery_buildout} </span>
                </div>

                <div class="stat-box">
                    <span class="stat-label"> 🔁 Rec. construcción </span>
                    <span class="stat-value">${stats.recovery_build} </span>
                </div>

                <div class="stat-box">
                    <span class="stat-label"> 🔁 Rec. finalización </span>
                    <span class="stat-value">${stats.recovery_finish}</span>
                </div>
            </div>
        </div>

        <div class="team-stats-section">
            <h3>Disciplina</h3>
            <div class="stats-grid">
                <div class="stat-box">
                    <span class="stat-label">🤕 F. cometidas </span>
                    <span class="stat-value"> ${stats.foul_committed}</span>
                </div>

                <div class="stat-box">
                    <span class="stat-label"> 🙋 F. sufridas</span>
                    <span class="stat-value">${stats.foul_received}</span>
                </div>

                <div class="stat-box">
                    <span class="stat-label">🟨 Amarillas</span>
                    <span class="stat-value">${stats.yellow}</span>
                </div>
            </div>
        </div>
    `;
}
