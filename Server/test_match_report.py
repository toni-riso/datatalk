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
        {"eventType": "rival_shot_off", "team": "away"}
    ])
    team_stats = build_team_stats(events)

    comparison = build_match_comparison(team_stats)

    assert comparison.loc["Goles", "Local"] == 1
    assert comparison.loc["Tiros totales", "Local"] == 3
    assert comparison.loc["Precisión de tiro", "Local"] == "66.7% (2/3)"
    assert comparison.loc["Conversión de tiro", "Local"] == "33.3% (1/3)"
    assert comparison.loc["Éxito en salida", "Local"] == "100.0% (1/1)"
    assert comparison.loc["Precisión de tiro", "Visitante"] == "0.0% (0/1)"
    assert comparison.loc["Éxito en salida", "Visitante"] == "—"


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
