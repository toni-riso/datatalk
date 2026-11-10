import pandas as pd


TIMELINE_EVENTS = {
    "goal_own": ("⚽ Gol", "Nuestro equipo"),
    "rival_goal": ("⚽ Gol rival", "Rival"),
    "goal_rival": ("⚽ Gol rival", "Rival"),
    "shot_target": ("🎯 Tiro a puerta", "Nuestro equipo"),
    "shot_off": ("Tiro fuera", "Nuestro equipo"),
    "rival_shot_target": ("🎯 Tiro a puerta", "Rival"),
    "rival_shot_off": ("Tiro fuera", "Rival"),
    "corner_for": ("🚩 Córner a favor", "Nuestro equipo"),
    "rival_corner": ("🚩 Córner en contra", "Rival"),
    "corner_against": ("🚩 Córner en contra", "Rival"),
    "assist": ("🅰️ Asistencia", "Nuestro equipo"),
    "yellow": ("🟨 Tarjeta amarilla", "Nuestro equipo"),
    "rival_yellow": ("🟨 Tarjeta amarilla", "Rival"),
    "substitution": ("🔄 Cambio", "Nuestro equipo")
}


def _event_second(event):
    match_second = event.get("matchSecond")
    if match_second is not None and not pd.isna(match_second):
        return int(match_second)

    minute = event.get("minute", 0)
    second = event.get("second", 0)
    return int(minute or 0) * 60 + int(second or 0)


def _event_player(event, event_type):
    if event_type == "substitution":
        player_out = event.get("playerOutName")
        player_in = event.get("playerInName")
        if player_out or player_in:
            return f"{player_out or '—'} → {player_in or '—'}"
        return event.get("description", "")
    return event.get("playerName") or ""


def build_match_timeline(events_df):
    """Build a chronological, score-aware timeline of key match events."""
    columns = ["Tiempo", "Marcador", "Evento", "Equipo", "Jugador"]
    timeline_events = []

    for order, event in enumerate(events_df.to_dict("records")):
        event_type = event.get("eventType")
        if event_type not in TIMELINE_EVENTS:
            continue

        match_second = _event_second(event)
        event_label, team_label = TIMELINE_EVENTS[event_type]
        timeline_events.append({
            "second": match_second,
            "order": order,
            "eventType": event_type,
            "Evento": event_label,
            "Equipo": team_label,
            "Jugador": _event_player(event, event_type)
        })

    timeline_events.sort(key=lambda event: (event["second"], event["order"]))
    own_goals = 0
    rival_goals = 0
    rows = []

    for event in timeline_events:
        event_type = event["eventType"]
        if event_type == "goal_own":
            own_goals += 1
        elif event_type in ("rival_goal", "goal_rival"):
            rival_goals += 1

        minute, second = divmod(event["second"], 60)
        rows.append({
            "Tiempo": f"{minute:02d}:{second:02d}",
            "Marcador": f"{own_goals}-{rival_goals}",
            "Evento": event["Evento"],
            "Equipo": event["Equipo"],
            "Jugador": event["Jugador"]
        })

    return pd.DataFrame(rows, columns=columns)
