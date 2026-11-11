from src.analysis.match_timeline import build_match_timeline
from src.analysis.player_event_details import build_player_details_by_id
from src.analysis.player_metrics import build_player_stats
from src.analysis.team_event_details import build_team_event_details_by_side
from src.analysis.team_metrics import build_team_stats


def analyze_match(data):
    """Calculate all reusable statistics and details for one match."""
    match = data["match"].iloc[0]
    venue = match.get("venue")
    if venue not in ("home", "away"):
        venue = "home"

    players = data["players"]
    events = data["events"]
    player_ids = (
        players["id"].tolist()
        if "id" in players
        else []
    )
    return {
        "match": match,
        "our_venue": venue,
        "team_stats": build_team_stats(events, venue),
        "player_stats": build_player_stats(
            players,
            events,
            match["currentSecond"]
        ),
        "team_event_details": build_team_event_details_by_side(
            events,
            venue
        ),
        "player_details": build_player_details_by_id(events, player_ids),
        "timeline": build_match_timeline(events)
    }


def analyze_matches(matches):
    """Analyze the uploaded matches once each, preserving their order."""
    return [
        analyze_match(loaded_match["data"])
        for loaded_match in matches
    ]
