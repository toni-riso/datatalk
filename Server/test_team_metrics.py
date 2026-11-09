import pandas as pd

from src.analysis.team_metrics import build_team_stats


def test_current_client_events_are_counted_for_team():
    events_df = pd.DataFrame([
        {"eventType": "buildout_success"},
        {"eventType": "dribble_ok"},
        {"eventType": "shot_target"},
        {"eventType": "goal_own"},
        {"eventType": "rival_shot_target"},
        {"eventType": "goal_rival"},
        {"eventType": "assist"},
        {"eventType": "recovery_finish"},
        {"eventType": "loss_build"},
        {"eventType": "corner_for"},
        {"eventType": "corner_against"}
    ])

    stats = build_team_stats(events_df)

    assert stats["buildout_success"] == 1
    assert stats["dribble_ok"] == 1
    assert stats["shot_target"] == 2
    assert stats["goal_own"] == 1
    assert stats["rival_shot_target"] == 2
    assert stats["assist"] == 1
    assert stats["recoveries"] == 1
    assert stats["losses"] == 1
    assert stats["corner_for"] == 1
    assert stats["corner_against"] == 1


def test_empty_events_are_supported():
    assert build_team_stats(pd.DataFrame())["goal_own"] == 0
