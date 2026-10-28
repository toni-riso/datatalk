// storage.js

const STORAGE_KEY = "footballScoutState";

/** * Guarda todo el estado de la aplicación*/
function saveState() {
    try {
        const data = JSON.stringify(state);
        localStorage.setItem(
            STORAGE_KEY,
            data
        );
        console.log(
            "💾 Estado guardado"
        );
        return true;
    }
    catch(error) {
        console.error(
            "Error guardando estado:",
            error
        );
        return false;
    }
}

/** * Recupera el estado guardado*/
function loadState() {
    try {
        const savedData =
            localStorage.getItem(
                STORAGE_KEY
            );
        if (!savedData) {
            console.log(
                "📂 No existe estado guardado"
            );
            return false;
        }
        const restoredState =
            JSON.parse(savedData);
        Object.assign(
            state,
            restoredState
        );
        console.log(
            "✅ Estado recuperado"
        );
        return true;
    }
    catch(error) {
        console.error(
            "Error recuperando estado:",
            error
        );
        return false;
    }
}

/** * Borra el estado guardado */
function clearState() {
    try {
        localStorage.removeItem(
            STORAGE_KEY
        );
        console.log(
            "🗑 Estado eliminado"
        );
        return true;
    }
    catch(error) {
        console.error(
            "Error eliminando estado:",
            error
        );
        return false;
    }
}

/** * Comprobar si existe una partida guardada */
function hasSavedState() {
    return (
        localStorage.getItem(
            STORAGE_KEY
        ) !== null
    );
}

/*** Obtener tamaño ocupado */
function getStorageInfo() {
    const data =
        localStorage.getItem(
            STORAGE_KEY
        );
    if (!data) {
        return {
            exists: false,
            size: 0
        };
    }
    return {
        exists: true,
        size: data.length
    };
}

function newMatch() {
    const confirmed = confirm(
        "¿Deseas comenzar un nuevo partido?\n\n" +
        "Se perderán todos los datos del partido actual."
    );
    if (!confirmed) {
        return;
    }
    if (state.matchFinished) {
        const proceed = confirm(
            "Este partido ya ha finalizado.\n\n¿Has exportado el JSON?"
        );
        if (!proceed) {
            return;
        }
    }
    state.matchFinished = false;

    clearState();
    location.reload();

}
    