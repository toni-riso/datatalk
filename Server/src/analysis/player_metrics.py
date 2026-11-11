# src/analysis/player_metrics.py

import pandas as pd

from src.analysis.event_catalog import (
    PLAYER_METRIC_EVENT_TYPES,
    canonical_event_type,
    phase_event_types
)
from src.analysis.minutes import calculate_minutes_played


def _event_counts(events_df):
    if events_df.empty or "eventType" not in events_df:
        return pd.Series(dtype="int64")
    return events_df["eventType"].map(canonical_event_type).value_counts()


def _count_event_type(event_counts, event_type):
    return int(event_counts.get(canonical_event_type(event_type), 0))


def _count_player_metric(event_counts, metric):
    return sum(
        _count_event_type(event_counts, event_type)
        for event_type in PLAYER_METRIC_EVENT_TYPES.get(metric, ())
    )


def count_events(events_df, event_type):
    """Count a canonical event type, including its known aliases."""
    return _count_event_type(_event_counts(events_df), event_type)


def count_player_metric(events_df, metric):
    """Count all catalogued event types contributing to a player metric."""
    return _count_player_metric(_event_counts(events_df), metric)


def count_substitutions(player):
    """
    Calcula el número de cambios a partir
    de los stints del jugador.
    Ejemplos:
    1 stint  -> 0 cambios
    2 stints -> 1 cambio
    3 stints -> 2 cambios
    """
    substitutions = 0
    for stint in player.get("stints", []):
        if stint.get("out") is not None:
            substitutions += 1
    return substitutions


def build_player_stats(
    players_df,
    events_df,
    match_duration_seconds
):
    """
    Genera estadísticas individuales
    para todos los jugadores.
    """
    #print(sorted(events_df["eventType"].unique()))
    stats = []
    match_duration_minutes = match_duration_seconds / 60

    for _, player in players_df.iterrows():
        if events_df.empty or "playerId" not in events_df:
            player_events = events_df.iloc[0:0]
        else:
            player_events = events_df[
                events_df["playerId"] == player["id"]
            ]
        event_counts = _event_counts(player_events)

        # SHOOTING
        goals = _count_player_metric(event_counts, "goals")
        shots_target = _count_player_metric(event_counts, "shots_target")
        shots_off_target = _count_player_metric(
            event_counts,
            "shots_off_target"
        )
        legacy_shots = _count_player_metric(event_counts, "legacy_shots")
        shots_total = max(
            legacy_shots,
            shots_target + shots_off_target
        )
        shots_off_target = max(
            shots_off_target,
            shots_total - shots_target
        )
        shot_accuracy = (
            round(
                shots_target / shots_total * 100,
                1
            )
            if shots_total > 0
            else 0.0
        )

        assists = _count_player_metric(event_counts, "assists")

        # DEFENSIVE
        recoveries = sum(
            _count_event_type(event_counts, event_type)
            for event_type in phase_event_types("recoveries")
        )
        losses = sum(
            _count_event_type(event_counts, event_type)
            for event_type in phase_event_types("losses")
        )

        # DRIBBLES
        dribbles_ok = _count_player_metric(event_counts, "dribbles_ok")
        dribbles_bad = _count_player_metric(event_counts, "dribbles_bad")
        total_dribbles = (dribbles_ok + dribbles_bad)
        dribble_accuracy = (
            round(
                dribbles_ok / total_dribbles * 100,
                1
            )
            if total_dribbles > 0
            else 0.0
        )

        # FOULS
        fouls_committed = _count_player_metric(
            event_counts,
            "fouls_committed"
        )
        fouls_suffered = _count_player_metric(
            event_counts,
            "fouls_received"
        )

        # DISCIPLINE
        yellow_cards = _count_player_metric(event_counts, "yellow_cards")

        # PLAYING TIME
        exact_minutes_played = calculate_minutes_played(
            player,
            match_duration_seconds
        )
        minutes_played = round(exact_minutes_played, 1)
        participation = (
            round(
                exact_minutes_played /
                match_duration_minutes * 100,
                1
            )
            if match_duration_minutes > 0
            else 0.0
        )

        # SUBSTITUTIONS
        substitutions = count_substitutions(player)

        # ACTIVITY
        total_actions = len(player_events)
        stats.append({

            "Dorsal": player["dorsal"],
            "Jugador": player["name"],
            "Posición": player["position"],

            "Titular": player["starter"],

            "Min": minutes_played,
            "% Part.": participation,

            "Regates OK": dribbles_ok,
            "Regates KO": dribbles_bad,
            "% Regate": dribble_accuracy,

            "Tiros": shots_total,
            "Tiros Puerta": shots_target,
            "Tiros Fuera": shots_off_target,
            "% Tiros Puerta": shot_accuracy,

            "Goles": goals,
            "Asistencias": assists,

            "Recuperaciones": recoveries,
            "Pérdidas": losses,       

            "Faltas Com.": fouls_committed,
            "Faltas Rec.": fouls_suffered,

            "Amarillas": yellow_cards,

            "Cambios": substitutions,

            "Acciones": total_actions
        })

    if not stats:
        return pd.DataFrame()

    stats_df = pd.DataFrame(stats)

    stats_df = (
        stats_df
        .sort_values(
            by=["Min", "Acciones"],
            ascending=False
        )
        .reset_index(drop=True)
    )

    return stats_df
