from contextlib import ExitStack
from unittest.mock import patch

from src.analysis.match_analysis import analyze_matches
from src.analysis.match_timeline import build_match_timeline
from src.analysis.player_event_details import build_player_details_by_id
from src.analysis.player_metrics import build_player_stats
from src.analysis.season_event_details import build_season_event_details
from src.analysis.season_metrics import build_season_stats
from src.analysis.season_player_details import build_season_player_details
from src.analysis.team_event_details import build_team_event_details_by_side
from src.analysis.team_metrics import build_team_stats
from test_season_metrics import _loaded_match


def test_season_views_reuse_each_matches_analysis():
    matches = [
        _loaded_match(
            "home",
            1,
            0,
            9,
            [
                {
                    "playerId": 9,
                    "eventType": "goal_own",
                    "matchSecond": 60,
                    "playerName": "Pablo"
                },
                {
                    "playerId": 9,
                    "eventType": "recovery",
                    "matchSecond": 120
                }
            ]
        )
    ]

    with ExitStack() as stack:
        team_stats_builder = stack.enter_context(patch(
            "src.analysis.match_analysis.build_team_stats",
            wraps=build_team_stats
        ))
        player_stats_builder = stack.enter_context(patch(
            "src.analysis.match_analysis.build_player_stats",
            wraps=build_player_stats
        ))
        team_details_builder = stack.enter_context(patch(
            "src.analysis.match_analysis.build_team_event_details_by_side",
            wraps=build_team_event_details_by_side
        ))
        player_details_builder = stack.enter_context(patch(
            "src.analysis.match_analysis.build_player_details_by_id",
            wraps=build_player_details_by_id
        ))
        timeline_builder = stack.enter_context(patch(
            "src.analysis.match_analysis.build_match_timeline",
            wraps=build_match_timeline
        ))
        analyses = analyze_matches(matches)
        season_stats = build_season_stats(matches, analyses)
        event_details = build_season_event_details(
            matches,
            match_analyses=analyses
        )
        player_details = build_season_player_details(
            matches,
            9,
            "Pablo",
            match_analyses=analyses
        )

    assert team_stats_builder.call_count == 1
    assert player_stats_builder.call_count == 1
    assert team_details_builder.call_count == 1
    assert player_details_builder.call_count == 1
    assert timeline_builder.call_count == 1
    assert season_stats["team"]["goals"] == 1
    assert event_details["Recuperaciones"]["values"] == [0, 0, 0, 1]
    assert player_details["recoveries"] == [0, 0, 0, 1]
    assert player_details["timeline"]["Acción"].tolist() == [
        "Gol",
        "Recuperación · Sin especificar"
    ]
