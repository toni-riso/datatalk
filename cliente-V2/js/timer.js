// timer.js

let timerInterval = null;

/** * Formatea segundos en MM:SS  */

function formatTime(totalSeconds) {
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return (
        minutes.toString().padStart(2, "0") +
        ":" +
        seconds.toString().padStart(2, "0")
    );
}

/** Actualiza los relojes de pantalla  */

function updateTimerDisplay() {
    const formatted =
        formatTime(state.currentSecond);
    const timer =
        document.getElementById("timer");
    if (timer) {
        timer.textContent = formatted;
    }
    const stickyTimer =
        document.getElementById("stickyTimer");
    if (stickyTimer) {
        stickyTimer.textContent = formatted;
    }
}

/** Inicia el cronómetro */

function startTimer() {
    if (timerInterval !== null) {
        return;
    }
    if (!state.matchStartTimestamp) {
        state.matchStartTimestamp = Date.now();
    }
    if (state.pauseStartedTimestamp) {
        state.pausedTime +=
            Date.now() - state.pauseStartedTimestamp;

        state.pauseStartedTimestamp = null;
    }
    state.matchRunning = true;

    updateTimerDisplay();
    saveState();

    timerInterval = setInterval(() => {
        state.currentSecond = Math.floor(
            (
                Date.now()
                - state.matchStartTimestamp
                - state.pausedTime
            ) / 1000
        );
        updateTimerDisplay();
        if (state.currentSecond % 30 === 0) {
            saveState();
        }
    }, 1000);
}

/** Pausa el cronómetro */

function pauseTimer() {
    if (timerInterval === null) {
        return;
    }
    clearInterval(timerInterval);
    timerInterval = null;
    state.pauseStartedTimestamp = Date.now();
    state.matchRunning = false;

    saveState();
}

/** Reinicia el cronómetro  */

function resetTimer() {

    if (timerInterval !== null) {
        clearInterval(timerInterval);
        timerInterval = null;
    }

    state.currentSecond = 0;
    state.matchStartTimestamp = null;
    state.pausedTime = 0;
    state.pauseStartedTimestamp = null;
    state.matchRunning = false;

    updateTimerDisplay();
}

/** Finaliza el partido  */

function finishMatch() {
    const confirmed = confirm(
        `¿Finalizar partido?
        ${state.matchData.homeTeam}
        ${state.homeGoals} - ${state.awayGoals}
        ${state.matchData.awayTeam}
        ⏱ Tiempo:
        ${formatTime(state.currentSecond)}
        ⚠ Recuerda exportar el partido al finalizar.`
    );
    if (!confirmed) {
        return;
    }
    pauseTimer();

    state.matchFinished = true; //Bandera comprobar si partido finalizado antes de nuevo partido
    saveState();

    alert(
        `🏁 Partido finalizado
        Resultado final:
        ${state.matchData.homeTeam}
        ${state.homeGoals} - ${state.awayGoals}
        ${state.matchData.awayTeam}
        ⚠ No olvides exportar el JSON antes de iniciar un nuevo partido.`
        );
}
/** Devuelve el minuto actual  */

function getCurrentMinute() {
    return Math.floor(
        state.currentSecond / 60
    );
}

/** Devuelve el segundo actual  */

function getCurrentSecond() {
    return state.currentSecond % 60;
}

/** Indica si el cronómetro está en marcha  */

function isTimerRunning() {
    return timerInterval !== null;
}

/** Inicialización  */

function initializeTimer() {

    updateTimerDisplay();
    const startBtn = document.getElementById("startBtn");
    const pauseBtn = document.getElementById("pauseBtn");
    const resetBtn = document.getElementById("resetBtn");
    const finishBtn = document.getElementById("finishBtn");

    if (startBtn) {
        startBtn.addEventListener( "click",  startTimer);
    }
    if (pauseBtn) {
        pauseBtn.addEventListener("click",pauseTimer);
    }
    if (resetBtn) {
        resetBtn.addEventListener("click", resetTimer);
    }
    if (finishBtn) {
        finishBtn.addEventListener("click", finishMatch);
    }

    document.addEventListener(
        "visibilitychange",
        () => {
            if (document.visibilityState === "visible" && state.matchRunning) {
                state.currentSecond = Math.floor(
                    (
                        Date.now() -
                        state.matchStartTimestamp -
                        state.pausedTime
                    ) / 1000
                );
                updateTimerDisplay();
            }
        }
    );
    console.log(
        "✅ timer.js inicializado"
    );

    if (
        state.matchRunning &&
        state.matchStartTimestamp
    ) {
        updateElapsedTime();
        updateTimerDisplay();
    }
}