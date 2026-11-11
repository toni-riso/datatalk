import pandas as pd


PLAYER_EVENT_LABELS = {
    "goal_own": "Gol",
    "own_goal": "Gol",
    "shot_target": "Tiro a puerta",
    "shot_off": "Tiro fuera",
    "shot": "Tiro",
    "assist": "Asistencia",
    "dribble_ok": "Regate completado",
    "dribble_bad": "Regate fallido",
    "recovery_buildout": "Recuperación · Salida",
    "recovery_build": "Recuperación · Construcción",
    "recovery_finish": "Recuperación · Finalización",
    "recovery": "Recuperación · Sin especificar",
    "loss_buildout": "Pérdida · Salida",
    "loss_build": "Pérdida · Construcción",
    "loss_finish": "Pérdida · Finalización",
    "loss": "Pérdida · Sin especificar",
    "foul_committed": "Falta cometida",
    "foul_received": "Falta recibida",
    "yellow": "Tarjeta amarilla"
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


def build_player_event_details(events_df, player_id):
    """Return a player's events in match order with readable labels and time."""
    if events_df.empty or "playerId" not in events_df:
        player_events = events_df.iloc[0:0]
    else:
        player_events = events_df[events_df["playerId"] == player_id]

    rows = []
    for order, event in enumerate(player_events.to_dict("records")):
        match_second = _event_second(event)
        minute, second = divmod(match_second, 60)
        event_type = event.get("eventType")
        description = event.get("description")
        if description is None or pd.isna(description):
            description = ""
        rows.append({
            "_second": match_second,
            "_order": order,
            "Minuto": f"{minute}'" if second == 0 else f"{minute}:{second:02d}",
            "Acción": PLAYER_EVENT_LABELS.get(event_type, str(event_type)),
            "Detalle": description
        })

    for order, event in enumerate(events_df.to_dict("records")):
        if event.get("eventType") != "substitution":
            continue
        if player_id not in (event.get("playerOut"), event.get("playerIn")):
            continue
        match_second = _event_second(event)
        minute, second = divmod(match_second, 60)
        direction = (
            "Sale"
            if event.get("playerOut") == player_id
            else "Entra"
        )
        description = event.get("description")
        if description is None or pd.isna(description):
            description = ""
        rows.append({
            "_second": match_second,
            "_order": len(player_events) + order,
            "Minuto": f"{minute}'" if second == 0 else f"{minute}:{second:02d}",
            "Acción": f"Cambio · {direction}",
            "Detalle": description
        })

    return pd.DataFrame(
        sorted(rows, key=lambda row: (row["_second"], row["_order"])),
        columns=["_second", "_order", "Minuto", "Acción", "Detalle"]
    ).drop(columns=["_second", "_order"])


def build_player_recovery_counts(events_df, player_id, event_types):
    """Count recovery or loss events by phase, including legacy event types."""
    if events_df.empty or "playerId" not in events_df:
        return [0, 0, 0, 0]
    player_events = events_df[events_df["playerId"] == player_id]
    counts = player_events["eventType"].value_counts()
    return [
        int(counts.get(event_type, 0))
        for event_type in event_types
    ]
