import pandas as pd

from src.analysis.player_metrics import build_player_stats


def test_current_client_events_are_counted_for_player():
    players_df = pd.DataFrame([
        {
            "id": 1,
            "dorsal": 9,
            "name": "Pablo",
            "position": "DC",
            "starter": True,
            "stints": [
                {
                    "in": 0,
                    "out": None
                }
            ]
        }
    ])

    events_df = pd.DataFrame([

        # REGATES

        {
            "playerId": 1,
            "eventType": "dribble_ok"
        },
        {
            "playerId": 1,
            "eventType": "dribble_ok"
        },
        {
            "playerId": 1,
            "eventType": "dribble_ok"
        },
        {
            "playerId": 1,
            "eventType": "dribble_bad"
        },

        {"playerId": 1, "eventType": "shot_off"},
        {
            "playerId": 1,
            "eventType": "shot_target"
        },
        {"playerId": 1, "eventType": "goal_own"},
        {"playerId": 1, "eventType": "assist"},
        {"playerId": 1, "eventType": "recovery_build"},
        {"playerId": 1, "eventType": "loss_finish"}
    ])

    stats = build_player_stats(
        players_df,
        events_df,
        match_duration_seconds=3600
    )

    player = stats.iloc[0]
    assert player["Regates OK"] == 3
    assert player["Regates KO"] == 1
    assert player["Tiros"] == 3
    assert player["Tiros Puerta"] == 2
    assert player["Tiros Fuera"] == 1
    assert player["% Tiros Puerta"] == 66.7
    assert player["Goles"] == 1
    assert player["Asistencias"] == 1
    assert player["Recuperaciones"] == 1
    assert player["Pérdidas"] == 1
    assert "Acc/Min" not in stats.columns


def test_participation_uses_actual_match_duration():
    players_df = pd.DataFrame([
        {
            "id": 1,
            "dorsal": 9,
            "name": "Pablo",
            "position": "DC",
            "starter": True,
            "stints": [{"in": 0, "out": 30}]
        }
    ])

    stats = build_player_stats(
        players_df,
        pd.DataFrame(),
        match_duration_seconds=1800
    )

    assert stats.iloc[0]["% Part."] == 100.0
    assert stats.iloc[0]["Min"] == 30.0
    assert stats.iloc[0]["Acciones"] == 0


def test_full_match_participation_is_100_percent_for_non_minute_duration():
    players_df = pd.DataFrame([
        {
            "id": 1,
            "dorsal": 9,
            "name": "Pablo",
            "position": "DC",
            "starter": True,
            "stints": [{"in": 0, "out": None}]
        }
    ])

    stats = build_player_stats(
        players_df,
        pd.DataFrame(),
        match_duration_seconds=661
    )

    assert stats.iloc[0]["Min"] == 11.0
    assert stats.iloc[0]["% Part."] == 100.0


def test_stint_minutes_are_converted_to_seconds_for_multiple_stints():
    players_df = pd.DataFrame([
        {
            "id": 1,
            "dorsal": 9,
            "name": "Pablo",
            "position": "DC",
            "starter": True,
            "stints": [
                {"in": 0, "out": 16},
                {"in": 22, "out": None}
            ]
        }
    ])

    stats = build_player_stats(
        players_df,
        pd.DataFrame(),
        match_duration_seconds=3761
    )

    player = stats.iloc[0]
    assert player["Min"] == 56.7
    assert player["% Part."] == 90.4
