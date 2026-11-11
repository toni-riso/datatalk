import pandas as pd

from src.analysis.event_catalog import phase_metric_keys
from src.analysis.player_event_details import build_player_details_by_id
from src.analysis.season_event_details import format_match_label


def build_season_player_details(
    matches,
    dorsal,
    player_name,
    match_analyses=None
):
    """Collect a player's phase counts and event timeline across matches."""
    if match_analyses is not None and len(match_analyses) != len(matches):
        raise ValueError("match_analyses must align with matches")

    recovery_totals = [0] * len(phase_metric_keys("recoveries"))
    loss_totals = [0] * len(phase_metric_keys("losses"))
    timelines = []

    for index, loaded_match in enumerate(matches):
        data = loaded_match["data"]
        players = data["players"]
        player_rows = players[
            (players["dorsal"] == dorsal) &
            (players["name"] == player_name)
        ]
        if player_rows.empty:
            continue

        player_id = player_rows.iloc[0]["id"]
        events = data["events"]
        match = data["match"].iloc[0]
        match_name = format_match_label(match)

        player_details = (
            match_analyses[index]["player_details"].get(player_id)
            if match_analyses is not None
            else build_player_details_by_id(events, [player_id])[player_id]
        )
        if player_details is None:
            continue

        match_recoveries = player_details["recoveries"]
        recovery_totals = [
            total + current
            for total, current in zip(recovery_totals, match_recoveries)
        ]

        match_losses = player_details["losses"]
        loss_totals = [
            total + current
            for total, current in zip(loss_totals, match_losses)
        ]

        timeline = player_details["timeline"]
        if not timeline.empty:
            timeline.insert(0, "Partido", match_name)
            timelines.append(timeline)

    if timelines:
        event_timeline = pd.concat(timelines, ignore_index=True)
    else:
        event_timeline = pd.DataFrame(
            columns=["Partido", "Minuto", "Acción", "Detalle"]
        )

    return {
        "recoveries": recovery_totals,
        "losses": loss_totals,
        "timeline": event_timeline
    }
