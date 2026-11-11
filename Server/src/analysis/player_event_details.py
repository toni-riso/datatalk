import pandas as pd

from src.analysis.event_catalog import (
    PLAYER_EVENT_LABELS,
    canonical_event_type,
    phase_metric_keys,
    phase_event_types
)


def _event_second(event):
    match_second = event.get("matchSecond")
    if match_second is not None and not pd.isna(match_second):
        return int(match_second)

    minute = event.get("minute", 0)
    second = event.get("second", 0)
    minute = 0 if minute is None or pd.isna(minute) else minute
    second = 0 if second is None or pd.isna(second) else second
    return int(minute) * 60 + int(second)


def _empty_player_details():
    return {
        "recoveries": [0] * len(phase_metric_keys("recoveries")),
        "losses": [0] * len(phase_metric_keys("losses")),
        "timeline": pd.DataFrame(
            columns=["Minuto", "Acción", "Detalle"]
        )
    }


def build_player_details_by_id(events_df, player_ids):
    """Build every requested player's phase counts and timeline in one pass."""
    player_ids = list(player_ids)
    player_details = {
        player_id: {
            "recoveries": [0] * len(phase_metric_keys("recoveries")),
            "losses": [0] * len(phase_metric_keys("losses")),
            "timeline_rows": []
        }
        for player_id in player_ids
    }
    if not player_details or events_df.empty:
        return {
            player_id: _empty_player_details()
            for player_id in player_ids
        }

    recovery_indexes = {
        event_type: index
        for index, event_type in enumerate(phase_event_types("recoveries"))
    }
    loss_indexes = {
        event_type: index
        for index, event_type in enumerate(phase_event_types("losses"))
    }
    has_player_id = "playerId" in events_df
    records = events_df.to_dict("records")

    for order, event in enumerate(records):
        event_type = canonical_event_type(event.get("eventType"))
        player_id = event.get("playerId") if has_player_id else None
        if player_id in player_details:
            player_detail = player_details[player_id]
            for group, indexes in (
                ("recoveries", recovery_indexes),
                ("losses", loss_indexes)
            ):
                index = indexes.get(event_type)
                if index is not None:
                    player_detail[group][index] += 1

            if event_type is not None:
                match_second = _event_second(event)
                description = event.get("description")
                if description is None or pd.isna(description):
                    description = ""
                player_detail["timeline_rows"].append({
                    "_second": match_second,
                    "_order": order,
                    "Minuto": _format_minute(match_second),
                    "Acción": PLAYER_EVENT_LABELS.get(
                        event_type,
                        str(event_type)
                    ),
                    "Detalle": description
                })

        if event.get("eventType") != "substitution":
            continue
        match_second = _event_second(event)
        description = event.get("description")
        if description is None or pd.isna(description):
            description = ""
        for substituted_player_id, direction in (
            (event.get("playerOut"), "Sale"),
            (event.get("playerIn"), "Entra")
        ):
            player_detail = player_details.get(substituted_player_id)
            if player_detail is None:
                continue
            player_detail["timeline_rows"].append({
                "_second": match_second,
                "_order": len(records) + order,
                "Minuto": _format_minute(match_second),
                "Acción": f"Cambio · {direction}",
                "Detalle": description
            })

    result = {}
    for player_id, player_detail in player_details.items():
        rows = sorted(
            player_detail["timeline_rows"],
            key=lambda row: (row["_second"], row["_order"])
        )
        result[player_id] = {
            "recoveries": player_detail["recoveries"],
            "losses": player_detail["losses"],
            "timeline": pd.DataFrame(
                rows,
                columns=["_second", "_order", "Minuto", "Acción", "Detalle"]
            ).drop(columns=["_second", "_order"])
        }
    return result


def _format_minute(match_second):
    minute, second = divmod(match_second, 60)
    return f"{minute}'" if second == 0 else f"{minute}:{second:02d}"


def build_player_event_details(events_df, player_id):
    """Return a player's events in match order with readable labels and time."""
    return build_player_details_by_id(events_df, [player_id])[
        player_id
    ]["timeline"]


def build_player_recovery_counts(events_df, player_id, phase_group):
    """Count recovery or loss events by the catalog's ordered phases."""
    return build_player_details_by_id(events_df, [player_id])[
        player_id
    ][phase_group]
