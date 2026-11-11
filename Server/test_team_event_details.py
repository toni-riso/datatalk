import pandas as pd

from src.analysis.team_event_details import (
    build_event_chart_data,
    build_team_event_details
)


def test_team_event_details_are_chronological_and_include_minutes():
    events = pd.DataFrame([
        {
            "eventType": "shot_off",
            "team": "home",
            "matchSecond": 125,
            "playerName": "Ana"
        },
        {
            "eventType": "goal_own",
            "team": "home",
            "minute": 1,
            "second": 0,
            "playerName": "Luis"
        },
        {
            "eventType": "buildout_fail",
            "team": "home",
            "matchSecond": 30
        },
        {
            "eventType": "recovery_buildout",
            "team": "home",
            "matchSecond": 65,
            "playerName": "Marta"
        }
    ])

    details = build_team_event_details(events, "home")

    assert details["shots"].to_dict("records") == [
        {"Minuto": "1'", "Acción": "Gol", "Jugador": "Luis"},
        {"Minuto": "2:05", "Acción": "Tiro fuera", "Jugador": "Ana"}
    ]
    assert details["buildouts"].to_dict("records") == [
        {"Minuto": "0:30", "Acción": "Salida fallida", "Jugador": "—"}
    ]
    assert details["recoveries"].to_dict("records") == [
        {
            "Minuto": "1:05",
            "Acción": "Recuperación · Salida",
            "Jugador": "Marta"
        }
    ]


def test_opponent_events_follow_actual_venue():
    events = pd.DataFrame([
        {
            "eventType": "rival_shot_target",
            "team": "home",
            "minute": 8
        },
        {
            "eventType": "rival_buildout_success",
            "team": "home",
            "minute": 12
        }
    ])

    details = build_team_event_details(
        events,
        side="home",
        our_venue="away"
    )

    assert details["shots"]["Acción"].tolist() == ["Tiro a puerta"]
    assert details["buildouts"]["Acción"].tolist() == ["Salida exitosa"]
    assert details["recoveries"].empty


def test_team_event_details_normalize_legacy_aliases():
    events = pd.DataFrame([
        {"eventType": "own_goal", "matchSecond": 60},
        {"eventType": "goal_rival", "matchSecond": 120},
        {"eventType": "corner_against", "matchSecond": 180}
    ])

    details = build_team_event_details(events, "home")

    assert details["shots"]["Acción"].tolist() == ["Gol"]
    assert details["shots"].iloc[0]["Minuto"] == "1'"
    assert details["shots"].iloc[0]["Jugador"] == "—"
    assert build_team_event_details(events, "away")["shots"][
        "Acción"
    ].tolist() == ["Gol"]


def test_invalid_side_is_rejected():
    try:
        build_team_event_details(pd.DataFrame(), "unknown")
    except ValueError:
        return
    raise AssertionError("Invalid side must raise ValueError")


def test_shot_chart_counts_goals_as_on_target():
    events = pd.DataFrame([
        {"eventType": "goal_own", "matchSecond": 60},
        {"eventType": "shot_target", "matchSecond": 120},
        {"eventType": "shot_off", "matchSecond": 180}
    ])
    details = build_team_event_details(events, "home")

    labels, values, total = build_event_chart_data(details["shots"], "shots")

    assert labels == ["A puerta (incl. goles)", "Fuera"]
    assert values == [2, 1]
    assert total == 3


def test_recovery_chart_counts_each_phase_and_handles_empty_tables():
    events = pd.DataFrame([
        {"eventType": "recovery_buildout", "matchSecond": 60},
        {"eventType": "recovery_build", "matchSecond": 120},
        {"eventType": "recovery_finish", "matchSecond": 180}
    ])
    details = build_team_event_details(events, "home")

    labels, values, total = build_event_chart_data(
        details["recoveries"],
        "recoveries"
    )
    empty_labels, empty_values, empty_total = build_event_chart_data(
        build_team_event_details(pd.DataFrame(), "home")["shots"],
        "shots"
    )

    assert labels == ["Salida", "Construcción", "Finalización", "Sin especificar"]
    assert values == [1, 1, 1, 0]
    assert total == 3
    assert empty_labels == ["A puerta (incl. goles)", "Fuera"]
    assert empty_values == [0, 0]
    assert empty_total == 0
