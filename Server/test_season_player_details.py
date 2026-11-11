import pandas as pd

from src.analysis.season_player_details import build_season_player_details


def _loaded_match(match_id, player_id, events, include_player=True):
    match = {
        "id": match_id,
        "homeTeam": "Local",
        "awayTeam": "Visitante",
        "round": match_id,
        "date": f"2026-0{match_id}-01",
        "currentSecond": 5400,
        "venue": "home",
        "homeGoals": 1,
        "awayGoals": 0
    }
    players = (
        pd.DataFrame([{
            "id": player_id,
            "dorsal": 9,
            "name": "Pablo"
        }])
        if include_player
        else pd.DataFrame(columns=["id", "dorsal", "name"])
    )
    return {
        "data": {
            "match": pd.DataFrame([match]),
            "players": players,
            "events": pd.DataFrame(events)
        }
    }


def test_season_player_details_aggregate_phases_and_match_timeline():
    matches = [
        _loaded_match(
            1,
            101,
            [
                {
                    "playerId": 101,
                    "eventType": "recovery_buildout",
                    "matchSecond": 60
                },
                {
                    "playerId": 101,
                    "eventType": "loss",
                    "matchSecond": 120
                }
            ]
        ),
        _loaded_match(
            2,
            102,
            [
                {
                    "playerId": 102,
                    "eventType": "recovery_build",
                    "matchSecond": 90
                },
                {
                    "playerId": 102,
                    "eventType": "recovery_finish",
                    "matchSecond": 180
                },
                {
                    "playerId": 102,
                    "eventType": "loss_build",
                    "matchSecond": 240
                },
                {
                    "playerId": 102,
                    "eventType": "goal_own",
                    "matchSecond": 300
                }
            ]
        ),
        _loaded_match(3, 103, [], include_player=False)
    ]

    details = build_season_player_details(matches, 9, "Pablo")

    assert details["recoveries"] == [1, 1, 1, 0]
    assert details["losses"] == [0, 1, 0, 1]
    assert details["timeline"].to_dict("records") == [
        {
            "Partido": "J1 · Local vs Visitante · 2026-01-01",
            "Minuto": "1'",
            "Acción": "Recuperación · Salida",
            "Detalle": ""
        },
        {
            "Partido": "J1 · Local vs Visitante · 2026-01-01",
            "Minuto": "2'",
            "Acción": "Pérdida · Sin especificar",
            "Detalle": ""
        },
        {
            "Partido": "J2 · Local vs Visitante · 2026-02-01",
            "Minuto": "1:30",
            "Acción": "Recuperación · Construcción",
            "Detalle": ""
        },
        {
            "Partido": "J2 · Local vs Visitante · 2026-02-01",
            "Minuto": "3'",
            "Acción": "Recuperación · Finalización",
            "Detalle": ""
        },
        {
            "Partido": "J2 · Local vs Visitante · 2026-02-01",
            "Minuto": "4'",
            "Acción": "Pérdida · Construcción",
            "Detalle": ""
        },
        {
            "Partido": "J2 · Local vs Visitante · 2026-02-01",
            "Minuto": "5'",
            "Acción": "Gol",
            "Detalle": ""
        }
    ]


def test_season_player_without_events_has_empty_timeline():
    matches = [_loaded_match(1, 101, [], include_player=True)]

    details = build_season_player_details(matches, 9, "Pablo")

    assert details["recoveries"] == [0, 0, 0, 0]
    assert details["losses"] == [0, 0, 0, 0]
    assert details["timeline"].empty
