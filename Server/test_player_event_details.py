import pandas as pd

from src.analysis.player_event_details import (
    build_player_event_details,
    build_player_recovery_counts
)


def test_player_timeline_is_chronological_and_labeled():
    events = pd.DataFrame([
        {
            "playerId": 7,
            "eventType": "shot_off",
            "matchSecond": 125
        },
        {
            "playerId": 7,
            "eventType": "goal_own",
            "minute": 1,
            "second": 0
        },
        {
            "playerId": 8,
            "eventType": "foul_received",
            "matchSecond": 80
        },
        {
            "eventType": "substitution",
            "playerOut": 7,
            "playerIn": 8,
            "matchSecond": 300,
            "description": "7 → 8"
        }
    ])

    timeline = build_player_event_details(events, 7)

    assert timeline.to_dict("records") == [
        {"Minuto": "1'", "Acción": "Gol", "Detalle": ""},
        {"Minuto": "2:05", "Acción": "Tiro fuera", "Detalle": ""},
        {"Minuto": "5'", "Acción": "Cambio · Sale", "Detalle": "7 → 8"}
    ]


def test_player_recovery_counts_include_legacy_event():
    events = pd.DataFrame([
        {"playerId": 7, "eventType": "recovery_buildout"},
        {"playerId": 7, "eventType": "recovery"},
        {"playerId": 7, "eventType": "recovery_finish"},
        {"playerId": 7, "eventType": "loss_build"}
    ])

    assert build_player_recovery_counts(
        events,
        7,
        "recoveries"
    ) == [1, 0, 1, 1]
    assert build_player_recovery_counts(
        events,
        7,
        "losses"
    ) == [0, 1, 0, 0]


def test_player_with_no_events_has_empty_timeline_and_zero_counts():
    events = pd.DataFrame([
        {"playerId": 8, "eventType": "shot_off"}
    ])

    assert build_player_event_details(events, 7).empty
    assert build_player_recovery_counts(
        events,
        7,
        "recoveries"
    ) == [0, 0, 0, 0]


def test_player_timeline_normalizes_event_aliases_from_catalog():
    events = pd.DataFrame([
        {
            "playerId": 7,
            "eventType": "own_goal",
            "matchSecond": 60
        }
    ])

    timeline = build_player_event_details(events, 7)

    assert timeline["Acción"].tolist() == ["Gol"]
