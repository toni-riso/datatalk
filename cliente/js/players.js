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
    
    renderPlayerStats();

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
            //state.selectedPlayer.dorsal;
            `${state.selectedPlayer.dorsal} - ${state.selectedPlayer.name}`;
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

function createPlayer(
    dorsal,
    name,
    position
) {
    return {
        id: Date.now(),
        dorsal: parseInt(dorsal),
        name,
        position,
        starter: false,
        active: false,
        yellowCards: 0,
        stints: [],
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

    saveState();

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
    const selectedPlayers =
        document.querySelectorAll(
            ".starter-checkbox:checked"
        );
        
    // Deben existir exactamente 11 o 8 titulares
    if (
        selectedPlayers.length !==
        state.playersOnField
    ) {
        alert(
            `Debes seleccionar exactamente ${state.playersOnField} titulares.`
        );
        return;
    }

    // Reiniciar estado de todos los jugadores
    state.players.forEach(player => {
        player.starter = false;
        player.active = false;
        player.stints = [];
    });

    // Activar titulares
    selectedPlayers.forEach(checkbox => {
        const playerId =
            Number(
                checkbox.dataset.playerId
            );
        const player =
            state.players.find(
                p => p.id === playerId
            );
        if (!player) {
            return;
        }
        player.starter = true;
        player.active = true;
        // Primer periodo de juego
        player.stints.push({
            in: 0,
            out: null
        });
    });

    // Limpiar selección de jugador
    clearSelectedPlayer();

    // Actualizar interfaz
    renderFieldPlayers();
    renderSquad();

    // Colapsar Datos del Partido
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
        matchButton.textContent =
            "▶";
    }

    // Colapsar Convocatoria
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
        squadButton.textContent =
            "▶";
    }

    // Guardar automáticamente
    saveState();

    // Mensaje final
    alert(
        "✅ Alineación confirmada correctamente"
    );
    console.log(
        "Titulares activos:",
        state.players.filter(
            player => player.active
        )
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
            yellowCards: 0,
            stints: [],
            events: []
        };          
        state.players.push(
            player
        );
    });
    renderSquad();

    saveState();

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

    saveState();

}
