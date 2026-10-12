// players.js

function renderFieldPlayers() {
    const container =
        document.getElementById(
            "fieldPlayers"
        );
    if (!container) {
        return;
    }
    container.innerHTML = "";
    const activePlayers =
        state.players
            .filter(
                player => player.active
            )
            .sort(
                (a, b) =>
                    a.dorsal - b.dorsal
            );
    activePlayers.forEach(player => {
        const button =
            document.createElement("button");
        button.className =
            "player-btn";
        if (
            state.selectedPlayer &&
            state.selectedPlayer.id === player.id
        ) {
            button.classList.add(
                "selected"
            );
        }
        button.innerHTML = `
            <strong>${player.dorsal}</strong>
            <br>
            ${player.name}
        `;
        button.addEventListener(
            "click",
            () => {

                selectPlayer(
                    player.id
                );
            }
        );
        container.appendChild(
            button
        );
    });
}

function selectPlayer(playerId) {
    const player = state.players.find(
        p => p.id === playerId
    );
    if (!player) return;
    state.selectedPlayer = player;
    updateSelectedPlayer();
    renderFieldPlayers();
}

function updateSelectedPlayer() {
    const selectedPlayerLabel =
        document.getElementById("selectedPlayer");
    if (selectedPlayerLabel) {
        selectedPlayerLabel.textContent =
            `${state.selectedPlayer.dorsal} - ${state.selectedPlayer.name}`;
    }
    const stickyPlayer =
        document.getElementById("stickySelectedPlayer");
    if (stickyPlayer) {
        stickyPlayer.textContent =
            state.selectedPlayer.dorsal;
    }
}

function clearSelectedPlayer() {
    state.selectedPlayer = null;
    const selectedPlayerLabel =
        document.getElementById("selectedPlayer");
    if (selectedPlayerLabel) {
        selectedPlayerLabel.textContent =
            "Ninguno";
    }
    const stickyPlayer =
        document.getElementById("stickySelectedPlayer");
    if (stickyPlayer) {
        stickyPlayer.textContent = "-";
    }
    renderFieldPlayers();
}

function getActivePlayers() {
    return state.players.filter(
        player => player.active
    );

}

function createPlayer(dorsal, name, position) {
    return {
        id: Date.now(),
        dorsal: parseInt(dorsal),
        name: name,
        position: position,
        starter: false,
        active: false,
        captain: false,
        minutesPlayed: 0,
        yellowCards: 0,
        entryMinute: null,
        exitMinute: null,
        events: []
    };
}

function addPlayer() {
    const dorsal =
        document.getElementById("playerDorsal").value;
    const name =
        document.getElementById("playerName").value;
    const position =
        document.getElementById("playerPosition").value;
    if (!dorsal || !name) {
        alert(
            "Debes indicar dorsal y nombre"
        );
        return;
    }
    const player =
        createPlayer(
            dorsal,
            name,
            position
        );
    state.players.push(player);
    renderSquad();
    clearPlayerForm();
}

function clearPlayerForm() {
    document.getElementById(
        "playerDorsal"
    ).value = "";
    document.getElementById(
        "playerName"
    ).value = "";
    document.getElementById(
        "playerPosition"
    ).selectedIndex = 0;
}

function renderSquad() {

    const container = document.getElementById("playersList");
    if (!container) return;
    container.innerHTML = "";

    state.players
        .sort((a, b) =>
            a.dorsal - b.dorsal
        )
        .forEach(player => {

            const row =
                document.createElement("div");

            row.className =
                "player-row";

            row.innerHTML = `

                <label>

                    <input
                        type="checkbox"
                        class="starter-checkbox"
                        data-player-id="${player.id}"
                        ${player.starter ? "checked" : ""}>

                    ${player.dorsal} -
                    ${player.name}
                    (${player.position})

                </label>

                <button type="button" class="delete-player-btn" data-player-id="${player.id}"> 🗑️ </button>
            `;
            container.appendChild(row);
        });
    initializeDeleteButtons();
}

function initializePlayers() {
    // Añadir jugador
    const addPlayerBtn =
        document.getElementById(
            "addPlayerBtn"
        );
    if (addPlayerBtn) {
        addPlayerBtn.addEventListener(
            "click",
            addPlayer
        );
    }
    // Cargar convocatoria
    const loadLineupBtn =
        document.getElementById(
            "loadLineupBtn"
        );
    if (loadLineupBtn) {
        loadLineupBtn.addEventListener(
            "click",
            loadLineupFile
        );
    }
    // Confirmar alineación
    const confirmLineupBtn =
        document.getElementById(
            "confirmLineupBtn"
        );
    if (confirmLineupBtn) {
        confirmLineupBtn.addEventListener(
            "click",
            confirmLineup
        );
    }
    console.log(
        "✅ players.js inicializado"
    );
}

function confirmLineup() {
    const selectedPlayers = document.querySelectorAll(
        ".starter-checkbox:checked"
    );
    // Validar que haya exactamente 11 titulares
    if (selectedPlayers.length !== 11) {
        alert(
            "Debes seleccionar exactamente 11 titulares."
        );
        return;
    }
    // Reiniciar estado de todos los jugadores
    state.players.forEach(player => {
        player.starter = false;
        player.active = false;
        player.entryMinute = null;
        player.exitMinute = null;
    });
    // Activar titulares seleccionados
    selectedPlayers.forEach(checkbox => {
        const playerId = Number(
            checkbox.dataset.playerId
        );
        const player = state.players.find(
            p => p.id === playerId
        );
        if (!player) {
            return;
        }
        player.starter = true;
        player.active = true;
        player.entryMinute = 0;
        player.exitMinute = null;
    });
    // Limpiar jugador seleccionado
    clearSelectedPlayer();
    // Actualizar listado de jugadores activos
    renderFieldPlayers();
    // Colapsar sección Datos del Partido
    const matchContent =
        document.getElementById(
            "matchContent"
        );
    if (matchContent) {
        matchContent.classList.add(
            "collapsed"
        );
    }
    const matchButton =
        document.querySelector(
            '.collapse-btn[data-target="matchContent"]'
        );
    if (matchButton) {
        matchButton.textContent = "▶";
    }
    // Colapsar sección Convocatoria
    const squadContent =
        document.getElementById(
            "squadContent"
        );
    if (squadContent) {
        squadContent.classList.add(
            "collapsed"
        );
    }
    const squadButton =
        document.querySelector(
            '.collapse-btn[data-target="squadContent"]'
        );
    if (squadButton) {
        squadButton.textContent = "▶";
    }
    // Mostrar resumen en consola
    console.log(
        "Titulares confirmados:"
    );
    state.players
        .filter(player => player.starter)
        .forEach(player => {
            console.log(
                player.dorsal +
                " - " +
                player.name
            );
        });
    // Mensaje final
    alert(
        "✅ Alineación confirmada correctamente"
    );
}

function loadLineupFile() {
    const fileInput =
        document.getElementById(
            "lineupFile"
        );
    if (!fileInput) {
        alert(
            "No se encuentra el selector de fichero."
        );
        return;
    }
    if (!fileInput.files.length) {
        alert(
            "Selecciona un fichero primero."
        );
        return;
    }
    const file =
        fileInput.files[0];
    const reader =
        new FileReader();
    reader.onload = function(event) {
        parseLineupText(
            event.target.result
        );
    };
    reader.readAsText(
        file,
        "UTF-8"
    );
}

function parseLineupText(text) {
    state.players = [];
    const lines =
        text.split("\n");
    lines.forEach(line => {
        const value =
            line.trim();
        if (!value) {
            return;
        }
        const parts =
            value.split(";");
        if (parts.length < 4) {
            return;
        }
        const isStarter =
            parts[0] === "T";
        const dorsal =
            Number(parts[1]);
        const name =
            parts[2];
        const position =
            parts[3];
        const player = {
            id:
                Date.now() +
                Math.random(),     
            dorsal,
            name,
            position,
            starter: isStarter,
            active: false,
            entryMinute: null,
            exitMinute: null,
            events: []
        };          
        state.players.push(
            player
        );
    });
    renderSquad();
    alert(
        "✅ Convocatoria cargada correctamente"
    );
}

function initializeDeleteButtons() {
    const buttons =
        document.querySelectorAll(
            ".delete-player-btn"
        );
    buttons.forEach(button => {
        button.addEventListener(
            "click",
            () => {
                const playerId =
                    Number(
                        button.dataset.playerId
                    );
                deletePlayer(playerId);
            }
        );
    });
}

function deletePlayer(playerId) {
    const player =
        state.players.find(
            p => p.id === playerId
        );
    if (!player) return;
    if (
        !confirm(
            `¿Eliminar a ${player.name}?`
        )
    ) {
        return;
    }
    state.players =
        state.players.filter(
            p => p.id !== playerId
        );
    renderSquad();
}