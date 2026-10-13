const state = {

    matchRunning: false,
    currentSecond: 0,

    homeGoals: 0,
    awayGoals: 0,

    activeTeam: "home",

    selectedPlayer: null,

    starters: [],
    substitutes: [],
    /*activePlayers: [
        { id: 1, dorsal: 1, name: "Portero" },
        { id: 2, dorsal: 2, name: "LI" },
        { id: 3, dorsal: 3, name: "DFC" },
        { id: 4, dorsal: 4, name: "DFC" },
        { id: 5, dorsal: 5, name: "LD" },
    
        { id: 6, dorsal: 6, name: "MCI" },
        { id: 7, dorsal: 7, name: "MC" },
        { id: 11, dorsal: 11, name: "MC" },
        { id: 8, dorsal: 8, name: "MCD" },
    
        { id: 9, dorsal: 9, name: "DC" },
        { id: 10, dorsal: 10, name: "DC" }
        ],
    */
        players: [

            {
                id: 1,
                dorsal: 1,
                name: "Portero",
                position: "POR",
                starter: true,
                active: true,
                captain: false,
                minutesPlayed: 0,
                yellowCards: 0,
                entryMinute: 0,
                exitMinute: null,
                events: []
            },
        
            {
                id: 2,
                dorsal: 2,
                name: "Lateral Izquierdo",
                position: "LI",
                starter: true,
                active: true,
                captain: false,
                minutesPlayed: 0,
                yellowCards: 0,
                entryMinute: 0,
                exitMinute: null,
                events: []
            },
            {
                id: 3,
                dorsal: 3,
                name: "Defensa Central1",
                position: "DFC1",
                starter: true,
                active: true,
                captain: false,
                minutesPlayed: 0,
                yellowCards: 0,
                entryMinute: 0,
                exitMinute: null,
                events: []
            },
            {
                id: 4,
                dorsal: 4,
                name: "Defensa Central 2",
                position: "DFC2",
                starter: true,
                active: true,
                captain: false,
                minutesPlayed: 0,
                yellowCards: 0,
                entryMinute: 0,
                exitMinute: null,
                events: []
            },
            {
                id: 5,
                dorsal: 5,
                name: "Lateral Derecho",
                position: "LI",
                starter: true,
                active: true,
                captain: false,
                minutesPlayed: 0,
                yellowCards: 0,
                entryMinute: 0,
                exitMinute: null,
                events: []
            },
            {
                id: 6,
                dorsal: 6,
                name: "Mediocentro Izquierdo",
                position: "MCI",
                starter: true,
                active: true,
                captain: false,
                minutesPlayed: 0,
                yellowCards: 0,
                entryMinute: 0,
                exitMinute: null,
                events: []
            },
            {
                id:7,
                dorsal: 7,
                name: "Mediocentro1",
                position: "MCO1",
                starter: true,
                active: true,
                captain: false,
                minutesPlayed: 0,
                yellowCards: 0,
                entryMinute: 0,
                exitMinute: null,
                events: []
            },
            {
                id: 8,
                dorsal: 8,
                name: "Mediocentro2",
                position: "MCO2",
                starter: true,
                active: true,
                captain: false,
                minutesPlayed: 0,
                yellowCards: 0,
                entryMinute: 0,
                exitMinute: null,
                events: []
            },
            {
                id: 9,
                dorsal: 9,
                name: "Mediocentro Derecho",
                position: "MCD",
                starter: true,
                active: true,
                captain: false,
                minutesPlayed: 0,
                yellowCards: 0,
                entryMinute: 0,
                exitMinute: null,
                events: []
            },
            {
                id: 10,
                dorsal: 10,
                name: "Delantero",
                position: "DEL1",
                starter: true,
                active: true,
                captain: false,
                minutesPlayed: 0,
                yellowCards: 0,
                entryMinute: 0,
                exitMinute: null,
                events: []
            },
            {
                id: 11,
                dorsal: 11,
                name: "Delantero2",
                position: "DEL2",
                starter: true,
                active: true,
                captain: false,
                minutesPlayed: 0,
                yellowCards: 0,
                entryMinute: 0,
                exitMinute: null,
                events: []
            }
        ],
    events: [],
    timeline: [],

    matchData: {
        date: "",
        homeTeam: "",
        awayTeam: "",
        competition: ""
    }
};