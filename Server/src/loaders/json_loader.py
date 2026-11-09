# src/loaders/json_loader.py

import json
import os
import pandas as pd
from typing import BinaryIO, Union


def load_match(file_path: Union[str, os.PathLike, BinaryIO]):
    """
    Carga un partido Football Scout desde una ruta o un fichero abierto.

    Returns:
        {
            "match": DataFrame,
            "players": DataFrame,
            "events": DataFrame
        }
    """

    if isinstance(file_path, (str, os.PathLike)):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = json.load(file_path)

    match_df = pd.DataFrame([data["match"]])
    players_df = pd.DataFrame(data["players"])
    events_df = pd.DataFrame(data["events"])

    return {
        "match": match_df,
        "players": players_df,
        "events": events_df
    }