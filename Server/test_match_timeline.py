import pandas as pd

from src.analysis.match_timeline import build_match_timeline


def test_timeline_sorts_events_and_tracks_score():
    events = pd.DataFrame([
        {
            "minute": 2,
            "second": 30,
            "eventType": "goal_own",
            "playerName": "Ana"
        },
        {
            "minute": 1,
            "second": 5,
            "eventType": "rival_shot_target"
        },
        {
            "minute": 4,
            "second": 2,
            "eventType": "rival_goal"
        },
        {
            "minute": 5,
            "second": 0,
            "eventType": "substitution",
            "playerOutName": "Luis",
            "playerInName": "Pau"
        },
        {
            "minute": 3,
            "second": 10,
            "eventType": "recovery_build"
        }
    ])

    timeline = build_match_timeline(events)

    assert timeline["Tiempo"].tolist() == ["01:05", "02:30", "04:02", "05:00"]
    assert timeline["Evento"].tolist() == [
        "🎯 Tiro a puerta",
        "⚽ Gol",
        "⚽ Gol rival",
        "🔄 Cambio"
    ]
    assert timeline["Marcador"].tolist() == ["0-0", "1-0", "1-1", "1-1"]
    assert timeline["Equipo"].tolist() == [
        "Rival",
        "Nuestro equipo",
        "Rival",
        "Nuestro equipo"
    ]
    assert timeline.iloc[3]["Jugador"] == "Luis → Pau"


def test_timeline_supports_legacy_rival_goal_and_empty_events():
    events = pd.DataFrame([
        {"minute": 0, "second": 20, "eventType": "own_goal"},
        {"minute": 0, "second": 40, "eventType": "goal_rival"}
    ])

    timeline = build_match_timeline(events)

    assert timeline["Marcador"].tolist() == ["1-0", "1-1"]
    assert build_match_timeline(pd.DataFrame()).empty
