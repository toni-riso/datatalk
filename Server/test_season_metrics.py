import pandas as pd

from src.analysis.season_metrics import build_season_stats, filter_matches


def _loaded_match(
    venue,
    home_goals,
    away_goals,
    player_id,
    events,
    season="2627",
    competition="Liga"
):
    match = {
        "venue": venue,
        "homeGoals": home_goals,
        "awayGoals": away_goals,
        "currentSecond": 600,
        "season": season,
        "competition": competition
    }
    players = pd.DataFrame([
        {
            "id": player_id,
            "dorsal": 9,
            "name": "Pablo",
            "position": "DC",
            "starter": True,
            "stints": [{"in": 0, "out": None}]
        }
    ])
    return {
        "match": pd.Series(match),
        "data": {
            "match": pd.DataFrame([match]),
            "players": players,
            "events": pd.DataFrame(events)
        }
    }


def test_season_stats_aggregate_scores_team_events_and_players():
    matches = [
        _loaded_match(
            "home",
            2,
            0,
            1,
            [
                {
                    "eventType": "goal_own",
                    "team": "home",
                    "playerId": 1
                },
                {
                    "eventType": "goal_own",
                    "team": "home",
                    "playerId": 1
                },
                {
                    "eventType": "dribble_ok",
                    "team": "home",
                    "playerId": 1
                }
            ]
        ),
        _loaded_match(
            "away",
            1,
            3,
            101,
            [
                {
                    "eventType": "own_goal",
                    "team": "away",
                    "playerId": 101
                },
                {
                    "eventType": "own_goal",
                    "team": "away",
                    "playerId": 101
                },
                {
                    "eventType": "own_goal",
                    "team": "away",
                    "playerId": 101
                },
                {
                    "eventType": "rival_goal",
                    "team": "home",
                    "playerId": 101
                }
            ]
        )
    ]

    stats = build_season_stats(matches)

    assert stats["matches"] == 2
    assert (stats["wins"], stats["draws"], stats["losses"]) == (2, 0, 0)
    assert (stats["goals_for"], stats["goals_against"]) == (5, 1)
    assert stats["points"] == 6
    assert stats["goal_difference"] == 4
    assert stats["clean_sheets"] == 1
    assert stats["team"]["goals"] == 5
    assert stats["team"]["shots_target"] == 5
    assert stats["opponent"]["goals"] == 1
    assert stats["opponent"]["shots_target"] == 1

    player = stats["players"].iloc[0]
    assert player["Jugador"] == "Pablo"
    assert player["Partidos"] == 2
    assert player["Convocatorias"] == 2
    assert player["Goles"] == 5
    assert player["% Part."] == 100.0
    assert player["Regates OK"] == 1


def test_season_stats_support_empty_match_list():
    stats = build_season_stats([])

    assert stats["matches"] == 0
    assert stats["goals_for"] == 0
    assert stats["players"].empty


def test_matches_can_be_filtered_by_season_and_competition():
    matches = [
        _loaded_match("home", 1, 0, 1, [], "2627", "Liga"),
        _loaded_match("home", 1, 0, 2, [], "2627", "Copa"),
        _loaded_match("away", 0, 1, 3, [], "2526", "Liga")
    ]

    filtered = filter_matches(
        matches,
        season="2627",
        competition="Copa"
    )

    assert len(filtered) == 1
    assert filtered[0]["match"]["season"] == "2627"
    assert filtered[0]["match"]["competition"] == "Copa"


def test_filter_without_values_includes_all_matches():
    matches = [
        _loaded_match("home", 1, 0, 1, [], "2627", "Liga"),
        _loaded_match("away", 0, 1, 2, [], "2526", "Copa")
    ]

    filtered = filter_matches(matches)
    assert len(filtered) == 2
    assert filtered[0] is matches[0]
    assert filtered[1] is matches[1]
