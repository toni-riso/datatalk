# src/loaders/json_loader.py

import json
import pandas as pd


def load_match(file_path):
    """
    Carga un partido Football Scout.

    Returns:
        {
            "match": DataFrame,
            "players": DataFrame,
            "events": DataFrame
        }
    """

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    match_df = pd.DataFrame([data["match"]])
    players_df = pd.DataFrame(data["players"])
    events_df = pd.DataFrame(data["events"])

    return {
        "match": match_df,
        "players": players_df,
        "events": events_df
    }