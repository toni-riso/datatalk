const state = {

    playersOnField: 11,
    matchType: "F11",
    matchRunning: false,
    currentSecond: 0,
    
    matchStartTimestamp: null,
    pausedTime: 0,
    pauseStartedTimestamp: null,

    matchFinished: false,
    
    homeGoals: 0,
    awayGoals: 0,

    activeTeam: "home",

    selectedPlayer: null,

    starters: [],
    substitutes: [],
    players: [],
    maxPlayersOnField: 11,
    events: [],
    timeline: [],

    matchData: {
        id: "",
        season: "",
        round: "",
        venue: "",
        date: "",
        competition: "",
        matchType: "",
        homeTeam: "",
        awayTeam: ""
    }
};

function createPlayer(
    dorsal,
    name,
    position
){
    return {
        id: Date.now(),
        dorsal: parseInt(dorsal),
        name,
        position,
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
