import pandas as pd

from src.analysis.event_catalog import (
    TEAM_EVENT_CHARTS,
    TEAM_EVENT_DETAILS,
    canonical_event_type
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


def build_team_event_details_by_side(events_df, our_venue="home"):
    """Build event detail tables for both match sides in one event pass."""
    if our_venue not in ("home", "away"):
        raise ValueError("our_venue must be 'home' or 'away'")

    opponent_venue = "away" if our_venue == "home" else "home"
    details_by_side = {
        side: {
            "shots": [],
            "buildouts": [],
            "recoveries": []
        }
        for side in ("home", "away")
    }

    for order, event in enumerate(events_df.to_dict("records")):
        event_type = canonical_event_type(event.get("eventType"))
        definition = TEAM_EVENT_DETAILS.get(event_type)
        if definition is None:
            continue
        perspective, category, label = definition
        event_side = our_venue if perspective == "own" else opponent_venue

        match_second = _event_second(event)
        minute, second = divmod(match_second, 60)
        player_name = event.get("playerName")
        if player_name is None or pd.isna(player_name) or not player_name:
            player_name = "—"
        details_by_side[event_side][category].append({
            "_second": match_second,
            "_order": order,
            "Minuto": f"{minute}'" if second == 0 else f"{minute}:{second:02d}",
            "Acción": label,
            "Jugador": player_name
        })

    return {
        side: {
            category: pd.DataFrame(
                sorted(
                    events,
                    key=lambda event: (
                        event["_second"],
                        event["_order"]
                    )
                ),
                columns=[
                    "_second",
                    "_order",
                    "Minuto",
                    "Acción",
                    "Jugador"
                ]
            ).drop(columns=["_second", "_order"])
            for category, events in details.items()
        }
        for side, details in details_by_side.items()
    }


def build_team_event_details(events_df, side, our_venue="home"):
    """Return chronological shot, buildout, and recovery events for a side."""
    if side not in ("home", "away"):
        raise ValueError("side must be 'home' or 'away'")
    return build_team_event_details_by_side(
        events_df,
        our_venue
    )[side]


def build_event_chart_data(event_table, category):
    """Return labels, values, and total for a team's event donut chart."""
    chart_definition = TEAM_EVENT_CHARTS.get(category)
    if chart_definition is None:
        raise ValueError(f"Unsupported event chart category: {category}")

    counts = event_table["Acción"].value_counts()
    labels = list(chart_definition["labels"])
    values = [
        int(sum(counts.get(event_label, 0) for event_label in event_labels))
        for event_labels in chart_definition["count_groups"]
    ]

    return labels, values, sum(values)
