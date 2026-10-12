// export.js

function updateMatchData() {
    const date =
        document.getElementById(
            "matchDate"
        );
    const competition =
        document.getElementById(
            "competition"
        );
    const matchType =
        document.getElementById(
            "matchType"
        );
    const homeTeam =
        document.getElementById(
            "homeTeam"
        );
    const awayTeam =
        document.getElementById(
            "awayTeam"
        );
    state.matchData.date =
        date ? date.value : "";
    state.matchData.competition =
        competition ? competition.value : "";
    state.matchData.matchType =
        venue ? matchType.value : "";
    state.matchData.homeTeam =
        homeTeam ? homeTeam.value : "";
    state.matchData.awayTeam =
        awayTeam ? awayTeam.value : "";
}

function buildExportData() {
    return {
        exportedAt:
            new Date().toISOString(),
        match: {
            date:
                state.matchData.date,
            competition:
                state.matchData.competition,
            homeTeam:
                state.matchData.homeTeam,
            awayTeam:
                state.matchData.awayTeam,
            matchType:
                state.matchType,
            playersOnField:
                state.playersOnField,
            currentSecond:
                state.currentSecond,
            homeGoals:
                state.homeGoals,
            awayGoals:
                state.awayGoals
        },
        players:
            state.players,
        events:
            state.events
    };
}

function getExportFileName() {
    const date =
        state.matchData.date ||
        new Date()
            .toISOString()
            .split("T")[0];
    const home =
        state.matchData.homeTeam ||
        "equipo";
    const away =
        state.matchData.awayTeam ||
        "rival";
    return (
        date +
        "_" +
        home +
        "_vs_" +
        away +
        ".json"
    );
}

function exportMatch() {
    updateMatchData();
    const exportData =
        buildExportData();
    const json =
        JSON.stringify(
            exportData,
            null,
            2
        );
    const blob =
        new Blob(
            [json],
            {
                type:
                    "application/json"
            }
        );
    const url =
        URL.createObjectURL(
            blob
        );
    const link =
        document.createElement(
            "a"
        );
    link.href = url;
    link.download =
        getExportFileName();
    document.body.appendChild(
        link
    );
    link.click();
    document.body.removeChild(
        link
    );
    URL.revokeObjectURL(
        url
    );
    console.log(
        "✅ Partido exportado"
    );
}

function initializeExportButton() {
    const button =
        document.getElementById(
            "exportMatchBtn"
        );
    if (!button) {
        return;
    }
    button.addEventListener(
        "click",
        exportMatch
    );
}