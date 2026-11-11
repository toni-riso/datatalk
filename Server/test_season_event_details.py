import pandas as pd

from src.analysis.season_event_details import build_season_event_details
from test_season_metrics import _loaded_match


def test_season_event_totals_and_match_occurrences_follow_our_venue():
    matches = [
        _loaded_match(
            "home",
            2,
            1,
            1,
            [
                {"eventType": "goal_own", "team": "home"},
                {"eventType": "goal_own", "team": "home"},
                {"eventType": "shot_off", "team": "home"},
                {"eventType": "buildout_success", "team": "home"},
                {"eventType": "recovery_buildout", "team": "home"},
                {"eventType": "loss_build", "team": "home"},
                {"eventType": "foul_committed", "team": "home"},
                {"eventType": "foul_received", "team": "home"}
            ]
        ),
        _loaded_match(
            "away",
            1,
            3,
            2,
            [
                {"eventType": "own_goal", "team": "away"},
                {"eventType": "own_goal", "team": "away"},
                {"eventType": "own_goal", "team": "away"},
                {"eventType": "rival_goal", "team": "home"},
                {"eventType": "rival_shot_off", "team": "home"},
                {"eventType": "rival_buildout_fail", "team": "home"},
                {"eventType": "recovery_build", "team": "away"},
                {"eventType": "loss_finish", "team": "away"},
                {"eventType": "foul_received", "team": "away"}
            ]
        )
    ]

    details = build_season_event_details(matches)

    assert details["Goles"]["values"] == [5, 2]
    assert details["Tiros"]["values"] == [5, 1]
    assert details["Salidas"]["values"] == [1, 0]
    assert details["Recuperaciones"]["values"] == [1, 1, 0]
    assert details["Pérdidas"]["values"] == [0, 1, 1]
    assert details["Faltas"]["values"] == [1, 2]

    goals_by_match = details["Goles"]["matches"]
    assert goals_by_match["Cantidad"].sum() == 7
    assert set(goals_by_match["Evento"]) == {
        "Goles a favor",
        "Goles en contra"
    }
    assert details["Recuperaciones"]["matches"]["Cantidad"].sum() == 2
    assert details["Pérdidas"]["matches"]["Cantidad"].sum() == 2
    assert details["Faltas"]["matches"]["Cantidad"].sum() == 3


def test_empty_event_categories_have_empty_occurrence_tables():
    match = _loaded_match("home", 0, 0, 1, [])

    details = build_season_event_details([match])

    for category in details.values():
        assert category["total"] == 0
        assert category["matches"].empty


def test_opponent_details_include_tracked_categories_and_mark_others():
    matches = [
        _loaded_match(
            "home",
            2,
            1,
            1,
            [
                {"eventType": "rival_goal", "team": "away"},
                {"eventType": "rival_shot_off", "team": "away"},
                {"eventType": "rival_buildout_success", "team": "away"}
            ]
        ),
        _loaded_match(
            "away",
            1,
            3,
            2,
            [
                {"eventType": "own_goal", "team": "away"},
                {"eventType": "own_goal", "team": "away"},
                {"eventType": "own_goal", "team": "away"},
                {"eventType": "rival_goal", "team": "home"},
                {"eventType": "rival_shot_target", "team": "home"},
                {"eventType": "rival_buildout_fail", "team": "home"}
            ]
        )
    ]

    details = build_season_event_details(matches, side="opponent")

    assert details["Goles"]["labels"] == [
        "Goles a favor del rival",
        "Goles en contra del rival"
    ]
    assert details["Goles"]["values"] == [2, 5]
    assert details["Tiros"]["values"] == [3, 1]
    assert details["Salidas"]["values"] == [1, 1]
    assert details["Goles"]["matches"]["Cantidad"].sum() == 7
    assert details["Tiros"]["matches"]["Cantidad"].sum() == 4
    assert details["Salidas"]["matches"]["Cantidad"].sum() == 2
    for category in ("Recuperaciones", "Pérdidas", "Faltas"):
        assert details[category]["tracked"] is False
        assert details[category]["total"] == 0
        assert details[category]["matches"].empty


def test_invalid_season_event_side_is_rejected():
    try:
        build_season_event_details([], side="unknown")
    except ValueError:
        return
    raise AssertionError("Invalid season event side must raise ValueError")
