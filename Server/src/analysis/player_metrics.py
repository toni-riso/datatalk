# src/analysis/player_metrics.py

import pandas as pd
from src.analysis.minutes import calculate_minutes_played

def count_events(events_df, event_type):
    """
    Cuenta eventos de un determinado tipo.
    """
    if events_df.empty or "eventType" not in events_df:
        return 0
    return len(
        events_df[
            events_df["eventType"] == event_type
        ]
    )


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

        # SHOOTING
        goals = count_events(player_events, "goal_own")
        shots_target = (
            count_events(player_events, "shot_target") +
            goals
        )
        shots_off_target = count_events(player_events, "shot_off")
        legacy_shots = count_events(player_events, "shot")
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

        assists = count_events(player_events, "assist")

        # DEFENSIVE
        recoveries = sum(
            count_events(player_events, event_type)
            for event_type in (
                "recovery_buildout",
                "recovery_build",
                "recovery_finish"
            )
        )
        if recoveries == 0:
            recoveries = count_events(player_events, "recovery")
        losses = sum(
            count_events(player_events, event_type)
            for event_type in (
                "loss_buildout",
                "loss_build",
                "loss_finish"
            )
        )
        if losses == 0:
            losses = count_events(player_events, "loss")

        # DRIBBLES
        dribbles_ok = count_events(player_events,"dribble_ok")
        dribbles_bad = count_events(player_events,"dribble_bad")
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
        fouls_committed = count_events(player_events,"foul_committed")
        fouls_suffered = count_events(player_events,"foul_received")

        # DISCIPLINE
        yellow_cards = count_events(player_events,"yellow")

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
