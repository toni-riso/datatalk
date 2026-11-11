import pandas as pd

from src.analysis.player_event_details import (
    build_player_event_details,
    build_player_recovery_counts
)
from src.analysis.season_event_details import format_match_label


def build_season_player_details(matches, dorsal, player_name):
    """Collect a player's phase counts and event timeline across matches."""
    recovery_totals = [0, 0, 0, 0]
    loss_totals = [0, 0, 0, 0]
    timelines = []

    for loaded_match in matches:
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

        match_recoveries = build_player_recovery_counts(
            events,
            player_id,
            (
                "recovery_buildout",
                "recovery_build",
                "recovery_finish",
                "recovery"
            )
        )
        if sum(match_recoveries[:3]) == 0:
            match_recoveries[:3] = [0, 0, 0]
        else:
            match_recoveries[3] = 0
        recovery_totals = [
            total + current
            for total, current in zip(recovery_totals, match_recoveries)
        ]

        match_losses = build_player_recovery_counts(
            events,
            player_id,
            ("loss_buildout", "loss_build", "loss_finish", "loss")
        )
        if sum(match_losses[:3]) == 0:
            match_losses[:3] = [0, 0, 0]
        else:
            match_losses[3] = 0
        loss_totals = [
            total + current
            for total, current in zip(loss_totals, match_losses)
        ]

        timeline = build_player_event_details(events, player_id)
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
