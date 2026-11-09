import pandas as pd

from src.analysis.team_metrics import build_team_stats


def test_current_client_events_are_counted_for_team():
    events_df = pd.DataFrame([
        {"eventType": "buildout_success", "team": "home"},
        {"eventType": "dribble_ok", "team": "home"},
        {"eventType": "shot_target", "team": "home"},
        {"eventType": "goal_own", "team": "home"},
        {"eventType": "rival_shot_target", "team": "away"},
        {"eventType": "rival_goal", "team": "away"},
        {"eventType": "assist", "team": "home"},
        {"eventType": "recovery_finish", "team": "home"},
        {"eventType": "loss_build", "team": "home"},
        {"eventType": "corner_for", "team": "home"},
        {"eventType": "rival_corner", "team": "away"}
    ])

    stats = build_team_stats(events_df)

    assert stats["home"]["buildout_success"] == 1
    assert stats["home"]["dribble_ok"] == 1
    assert stats["home"]["shots_target"] == 2
    assert stats["home"]["goals"] == 1
    assert stats["home"]["assists"] == 1
    assert stats["home"]["recoveries"] == 1
    assert stats["home"]["losses"] == 1
    assert stats["home"]["corners_for"] == 1
    assert stats["away"]["shots_target"] == 2
    assert stats["away"]["goals"] == 1
    assert stats["away"]["corners_for"] == 1
    assert stats["mismatched_team_labels"] == 0


def test_our_team_metrics_follow_venue_when_playing_away():
    events_df = pd.DataFrame([
        {"eventType": "goal_own", "team": "away"},
        {"eventType": "rival_goal", "team": "home"},
        {"eventType": "corner_for", "team": "away"},
        {"eventType": "rival_corner", "team": "home"}
    ])

    stats = build_team_stats(events_df, our_venue="away")

    assert stats["away"]["goals"] == 1
    assert stats["home"]["goals"] == 1
    assert stats["away"]["corners_for"] == 1
    assert stats["home"]["corners_for"] == 1
    assert stats["our_venue"] == "away"


def test_legacy_rival_event_type_overrides_stale_team_label():
    events_df = pd.DataFrame([
        {"eventType": "goal_rival", "team": "home"},
        {"eventType": "corner_against", "team": "home"},
        {"eventType": "rival_shot_target", "team": "home"}
    ])

    stats = build_team_stats(events_df, our_venue="home")

    assert stats["away"]["goals"] == 1
    assert stats["away"]["shots_target"] == 2
    assert stats["away"]["corners_for"] == 1
    assert stats["mismatched_team_labels"] == 3


def test_empty_events_are_supported():
    stats = build_team_stats(pd.DataFrame())
    assert stats["home"]["goals"] == 0
    assert stats["away"]["goals"] == 0


def test_invalid_venue_is_rejected():
    try:
        build_team_stats(pd.DataFrame(), our_venue="unknown")
    except ValueError:
        return
    raise AssertionError("Invalid venue must raise ValueError")
