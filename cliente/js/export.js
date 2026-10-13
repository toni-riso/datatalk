// export.js

function updateMatchData() {
    state.matchData.id =
        document.getElementById(
            "matchId"
        )?.value || "";

    state.matchData.season =
        document.getElementById(
            "season"
        )?.value || "";
    state.matchData.round =
        Number(
            document.getElementById(
                "round"
            )?.value || 1
        );
    state.matchData.venue =
        document.getElementById(
            "venue"
        )?.value || "home";
    state.matchData.date =
        document.getElementById(
            "matchDate"
        )?.value || "";
    state.matchData.competition =
        document.getElementById(
            "competition"
        )?.value || "";
    state.matchData.homeTeam =
        document.getElementById(
            "homeTeam"
        )?.value || "";
    state.matchData.awayTeam =
        document.getElementById(
            "awayTeam"
        )?.value || "";
}

function buildExportData() {
    return {
        exportedAt:
            new Date().toISOString(),
        match: {
            id:
                state.matchData.id,
            season:
                state.matchData.season,
            round:
                state.matchData.round,
            venue:
                state.matchData.venue,
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

function generateMatchId() {
    updateMatchData();
    const date =
        state.matchData.date || "";
    const homeTeam =
        (state.matchData.homeTeam || "")
            .trim()
            .toUpperCase()
            .replaceAll(" ", "-");
    const awayTeam =
        (state.matchData.awayTeam || "")
            .trim()
            .toUpperCase()
            .replaceAll(" ", "-");
    state.matchData.id =
        `${date}-${homeTeam}-${awayTeam}`;
}
