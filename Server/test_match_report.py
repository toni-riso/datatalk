import pandas as pd

from src.analysis.match_report import (
    build_match_comparison,
    get_score_discrepancies
)
from src.analysis.team_metrics import build_team_stats


def test_match_comparison_includes_volumes_with_percentages():
    events = pd.DataFrame([
        {"eventType": "goal_own", "team": "home"},
        {"eventType": "shot_target", "team": "home"},
        {"eventType": "shot_off", "team": "home"},
        {"eventType": "buildout_success", "team": "home"},
        {"eventType": "rival_shot_off", "team": "away"},
        {"eventType": "recovery_buildout", "team": "home"},
        {"eventType": "recovery_build", "team": "home"},
        {"eventType": "recovery_finish", "team": "home"},
        {"eventType": "loss_buildout", "team": "home"},
        {"eventType": "loss_build", "team": "home"},
        {"eventType": "loss_finish", "team": "home"},
        {"eventType": "corner_for", "team": "home"},
        {"eventType": "rival_corner", "team": "away"}
    ])
    team_stats = build_team_stats(events)

    comparison = build_match_comparison(team_stats)

    home = "Local"
    away = "Visitante"

    assert comparison.loc[home, ("Tiros y córners", "Goles")] == 1
    assert comparison.loc[home, ("Tiros y córners", "Tiros totales")] == 3
    assert comparison.loc[
        home, ("Tiros y córners", "Precisión de tiro")
    ] == "66.7% (2/3)"
    assert "Conversión de tiro" not in comparison.columns.get_level_values(
        "Estadística"
    )
    assert comparison.loc[home, ("Salidas", "Éxito en salida")] == "100.0% (1/1)"
    assert comparison.loc[
        away, ("Tiros y córners", "Precisión de tiro")
    ] == "0.0% (0/1)"
    assert comparison.loc[away, ("Salidas", "Éxito en salida")] == "—"
    assert comparison.loc[home, ("Recuperaciones", "Salida")] == 1
    assert comparison.loc[home, ("Recuperaciones", "Construcción")] == 1
    assert comparison.loc[home, ("Recuperaciones", "Finalización")] == 1
    assert comparison.loc[home, ("Pérdidas", "Salida")] == 1
    assert comparison.loc[home, ("Pérdidas", "Construcción")] == 1
    assert comparison.loc[home, ("Pérdidas", "Finalización")] == 1
    assert comparison.loc[away, ("Recuperaciones", "Salida")] == "—"
    assert comparison.loc[away, ("Pérdidas", "Salida")] == "—"
    assert comparison.loc[home, ("Tiros y córners", "Córners")] == 1
    assert comparison.loc[away, ("Tiros y córners", "Córners")] == 1


def test_match_comparison_includes_team_names_in_column_labels():
    team_stats = build_team_stats(pd.DataFrame())

    comparison = build_match_comparison(
        team_stats,
        home_team="Barrio Obrero C",
        away_team="San Gabriel A"
    )

    assert list(comparison.index) == [
        "Local (Barrio Obrero C)",
        "Visitante (San Gabriel A)"
    ]


def test_recoveries_and_losses_follow_our_venue():
    events = pd.DataFrame([
        {"eventType": "recovery_buildout", "team": "away"},
        {"eventType": "loss_finish", "team": "away"}
    ])
    team_stats = build_team_stats(events, our_venue="away")

    comparison = build_match_comparison(team_stats)

    assert comparison.loc["Visitante", ("Recuperaciones", "Salida")] == 1
    assert comparison.loc["Visitante", ("Pérdidas", "Finalización")] == 1
    assert comparison.loc["Local", ("Recuperaciones", "Salida")] == "—"
    assert comparison.loc["Local", ("Pérdidas", "Salida")] == "—"


def test_score_discrepancies_only_report_mismatched_sides():
    events = pd.DataFrame([
        {"eventType": "goal_own", "team": "home"},
        {"eventType": "rival_goal", "team": "away"}
    ])
    team_stats = build_team_stats(events)

    assert get_score_discrepancies(team_stats, 1, 0) == [
        {
            "side": "Visitante",
            "score_goals": 0,
            "event_goals": 1
        }
    ]


def test_away_match_score_is_compared_using_actual_home_and_away_sides():
    events = pd.DataFrame([
        {"eventType": "own_goal", "team": "away"},
        {"eventType": "own_goal", "team": "away"},
        {"eventType": "rival_goal", "team": "home"}
    ])
    match = {
        "venue": "away",
        "homeGoals": 1,
        "awayGoals": 2
    }
    team_stats = build_team_stats(events, match["venue"])

    assert get_score_discrepancies(
        team_stats,
        match["homeGoals"],
        match["awayGoals"]
    ) == []
