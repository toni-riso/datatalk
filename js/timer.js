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
    state.matchRunning = true;
    timerInterval = setInterval(() => {
        state.currentSecond++;
        updateTimerDisplay();
    }, 1000);
}

/** Pausa el cronómetro */

function pauseTimer() {
    if (timerInterval === null) {
        return;
    }
    clearInterval(timerInterval);
    timerInterval = null;
    state.matchRunning = false;
}

/** Reinicia el cronómetro  */

function resetTimer() {
    pauseTimer();
    state.currentSecond = 0;
    updateTimerDisplay();
}

/** Finaliza el partido  */

function finishMatch() {
    pauseTimer();
    alert(
        "🏁 Partido finalizado\n\n" +
        "Resultado: " +
        state.homeGoals +
        " - " +
        state.awayGoals
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
    const startBtn =
        document.getElementById("startBtn");
    const pauseBtn =
        document.getElementById("pauseBtn");
    const resetBtn =
        document.getElementById("resetBtn");
    const finishBtn =
        document.getElementById("finishBtn");
    if (startBtn) {
        startBtn.addEventListener(
            "click",
            startTimer
        );
    }
    if (pauseBtn) {
        pauseBtn.addEventListener(
            "click",
            pauseTimer
        );
    }
    if (resetBtn) {
        resetBtn.addEventListener(
            "click",
            resetTimer
        );
    }
    if (finishBtn) {
        finishBtn.addEventListener(
            "click",
            finishMatch
        );
    }
    console.log(
        "✅ timer.js inicializado"
    );
}