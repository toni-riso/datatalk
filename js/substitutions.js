function initializeSubstitutions() {
    const button =
        document.getElementById(
            "substitutionBtn"
        );
    if (!button) return;
    button.addEventListener(
        "click",
        openSubstitutionModal
    );
    document
        .getElementById(
            "cancelSubBtn"
        )
        ?.addEventListener(
            "click",
            closeSubstitutionModal
        );
    document
        .getElementById(
            "confirmSubBtn"
        )
        ?.addEventListener(
            "click",
            confirmSubstitution
        );
}

function openSubstitutionModal() {
    fillPlayersOut();
    fillPlayersIn();
    document
        .getElementById(
            "substitutionModal"
        )
        .classList.remove(
            "hidden"
        );
}

function fillPlayersOut() {
    const select =
        document.getElementById(
            "playerOutSelect"
        );
    select.innerHTML = "";
    state.players
        .filter(
            player => player.active
        )
        .forEach(player => {
            const option =
                document.createElement(
                    "option"
                );
            option.value =
                player.id;
            option.textContent =
                `${player.dorsal} - ${player.name}`;
            select.appendChild(
                option
            );
        });
}

function fillPlayersIn() {
    const select =
        document.getElementById(
            "playerInSelect"
        );
    select.innerHTML = "";
    state.players
        .filter(
            player => !player.active
        )
        .forEach(player => {
            const option =
                document.createElement(
                    "option"
                );
            option.value =
                player.id;
            option.textContent =
                `${player.dorsal} - ${player.name}`;
            select.appendChild(
                option
            );
        });
}

function confirmSubstitution() {
    const playerOutId =
        Number(
            document.getElementById(
                "playerOutSelect"
            ).value
        );
    const playerInId =
        Number(
            document.getElementById(
                "playerInSelect"
            ).value
        );
    const playerOut =
        state.players.find(
            player => player.id === playerOutId
        );
    const playerIn =
        state.players.find(
            player => player.id === playerInId
        );
    if (!playerOut || !playerIn) {
        alert(
            "Debes seleccionar los dos jugadores."
        );
        return;
    }
    const currentMinute =
        getCurrentMinute();
    // Sale del campo
    playerOut.active = false;
    playerOut.exitMinute =
        currentMinute;
    // Entra al campo
    playerIn.active = true;
    playerIn.entryMinute =
        currentMinute;
    // Registrar evento
    registerSubstitutionEvent(
        playerOut,
        playerIn
    );
    // Si el jugador que sale estaba seleccionado
    if (
        state.selectedPlayer &&
        state.selectedPlayer.id === playerOut.id
    ) {
        clearSelectedPlayer();
    }
    // Actualizar jugadores visibles
    renderFieldPlayers();
    // Cerrar modal
    closeSubstitutionModal();
}

function closeSubstitutionModal() {
    const modal =
        document.getElementById(
            "substitutionModal"
        );
    if (!modal) {
        return;
    }
    modal.classList.add("hidden");
    // Limpiar selects
    const playerOutSelect =
        document.getElementById(
            "playerOutSelect"
        );
    const playerInSelect =
        document.getElementById(
            "playerInSelect"
        );
    if (playerOutSelect) {
        playerOutSelect.innerHTML = "";
    }
    if (playerInSelect) {
        playerInSelect.innerHTML = "";
    }
}

function registerSubstitutionEvent(
    playerOut,
    playerIn
) {
    const event = {
        id: Date.now(),
        timestamp:
            new Date().toISOString(),
        matchSecond:
            state.currentSecond,
        minute:
            getCurrentMinute(),
        second:
            getCurrentSecond(),
        team:
            state.activeTeam,
        eventType:
            "substitution",
        playerOutId:
            playerOut.id,
        playerOutDorsal:
            playerOut.dorsal,
        playerOutName:
            playerOut.name,
        playerInId:
            playerIn.id,
        playerInDorsal:
            playerIn.dorsal,
        playerInName:
            playerIn.name
    };
    state.events.push(event);
    addTimelineEvent(event);
    console.log(
        "🔄 Cambio registrado",
        event
    );
}


