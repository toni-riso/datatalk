import io
import json

from src.loaders.json_loader import load_match


def test_load_match_accepts_uploaded_json_file():
    match_data = {
        "match": {
            "date": "2026-11-11",
            "homeTeam": "Gabriel-A",
            "awayTeam": "Camp-B"
        },
        "players": [{"id": 1, "name": "Jugador"}],
        "events": [{"eventType": "goal_own"}]
    }

    uploaded_file = io.BytesIO(
        json.dumps(match_data).encode("utf-8")
    )
    loaded_data = load_match(uploaded_file)

    assert loaded_data["match"].iloc[0]["homeTeam"] == "Gabriel-A"
    assert loaded_data["players"].iloc[0]["name"] == "Jugador"
    assert loaded_data["events"].iloc[0]["eventType"] == "goal_own"
