import pandas as pd

from src.analysis.player_metrics import build_player_stats

print ("INICIO TEST")
def test_shooting_and_dribbling():

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

        # TIROS

        {
            "playerId": 1,
            "eventType": "shot"
        },
        {
            "playerId": 1,
            "eventType": "shot"
        },
        {
            "playerId": 1,
            "eventType": "shot"
        },

        {
            "playerId": 1,
            "eventType": "shot_target"
        },
        {
            "playerId": 1,
            "eventType": "shot_target"
        }
    ])

    stats = build_player_stats(
        players_df,
        events_df,
        match_duration_seconds=3600,
        match_type="F8"
    )

    print(stats)
