import pandas as pd


OWN_EVENTS = {
    "goal_own": ("shots", "Gol"),
    "own_goal": ("shots", "Gol"),
    "shot_target": ("shots", "Tiro a puerta"),
    "shot_off": ("shots", "Tiro fuera"),
    "buildout_success": ("buildouts", "Salida exitosa"),
    "buildout_fail": ("buildouts", "Salida fallida"),
    "recovery_buildout": ("recoveries", "Recuperación · Salida"),
    "recovery_build": ("recoveries", "Recuperación · Construcción"),
    "recovery_finish": ("recoveries", "Recuperación · Finalización"),
    "recovery": ("recoveries", "Recuperación · Sin especificar")
}

OPPONENT_EVENTS = {
    "rival_goal": ("shots", "Gol"),
    "goal_rival": ("shots", "Gol"),
    "rival_shot_target": ("shots", "Tiro a puerta"),
    "rival_shot_off": ("shots", "Tiro fuera"),
    "rival_buildout_success": ("buildouts", "Salida exitosa"),
    "rival_buildout_fail": ("buildouts", "Salida fallida")
}


def _event_second(event):
    match_second = event.get("matchSecond")
    if match_second is not None and not pd.isna(match_second):
        return int(match_second)

    minute = event.get("minute", 0)
    second = event.get("second", 0)
    minute = 0 if minute is None or pd.isna(minute) else minute
    second = 0 if second is None or pd.isna(second) else second
    return int(minute) * 60 + int(second)


def build_team_event_details(events_df, side, our_venue="home"):
    """Return chronological shot, buildout, and recovery events for a side."""
    if side not in ("home", "away"):
        raise ValueError("side must be 'home' or 'away'")
    if our_venue not in ("home", "away"):
        raise ValueError("our_venue must be 'home' or 'away'")

    opponent_venue = "away" if our_venue == "home" else "home"
    details = {
        "shots": [],
        "buildouts": [],
        "recoveries": []
    }

    for order, event in enumerate(events_df.to_dict("records")):
        event_type = event.get("eventType")
        if event_type in OWN_EVENTS:
            event_side = our_venue
            category, label = OWN_EVENTS[event_type]
        elif event_type in OPPONENT_EVENTS:
            event_side = opponent_venue
            category, label = OPPONENT_EVENTS[event_type]
        else:
            continue

        if event_side != side:
            continue

        match_second = _event_second(event)
        minute, second = divmod(match_second, 60)
        player_name = event.get("playerName")
        if player_name is None or pd.isna(player_name) or not player_name:
            player_name = "—"
        details[category].append({
            "_second": match_second,
            "_order": order,
            "Minuto": f"{minute}'" if second == 0 else f"{minute}:{second:02d}",
            "Acción": label,
            "Jugador": player_name
        })

    return {
        category: pd.DataFrame(
            sorted(events, key=lambda event: (event["_second"], event["_order"])),
            columns=["_second", "_order", "Minuto", "Acción", "Jugador"]
        ).drop(columns=["_second", "_order"])
        for category, events in details.items()
    }


def build_event_chart_data(event_table, category):
    """Return labels, values, and total for a team's event donut chart."""
    counts = event_table["Acción"].value_counts()
    if category == "shots":
        labels = ["A puerta (incl. goles)", "Fuera"]
        values = [
            int(counts.get("Tiro a puerta", 0) + counts.get("Gol", 0)),
            int(counts.get("Tiro fuera", 0))
        ]
    elif category == "buildouts":
        labels = ["Exitosas", "Fallidas"]
        values = [
            int(counts.get("Salida exitosa", 0)),
            int(counts.get("Salida fallida", 0))
        ]
    elif category == "recoveries":
        recovery_labels = (
            "Recuperación · Salida",
            "Recuperación · Construcción",
            "Recuperación · Finalización",
            "Recuperación · Sin especificar"
        )
        labels = ["Salida", "Construcción", "Finalización", "Sin especificar"]
        values = [int(counts.get(label, 0)) for label in recovery_labels]
    else:
        raise ValueError(f"Unsupported event chart category: {category}")

    return labels, values, sum(values)
