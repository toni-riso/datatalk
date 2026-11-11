import pandas as pd

from src.analysis.season_metrics import get_match_filter_value
from src.analysis.team_metrics import build_team_stats


SEASON_EVENT_CATEGORIES = {
    "Goles": {
        "labels": ("Goles a favor", "Goles en contra"),
        "keys": ("goals_for", "goals_against")
    },
    "Tiros": {
        "labels": ("Tiros a puerta", "Tiros fuera"),
        "keys": ("shots_target", "shots_off")
    },
    "Salidas": {
        "labels": ("Exitosas", "Fallidas"),
        "keys": ("buildout_success", "buildout_fail")
    },
    "Recuperaciones": {
        "labels": ("Salida", "Construcción", "Finalización"),
        "keys": (
            "recovery_buildout",
            "recovery_build",
            "recovery_finish"
        )
    },
    "Pérdidas": {
        "labels": ("Salida", "Construcción", "Finalización"),
        "keys": ("loss_buildout", "loss_build", "loss_finish")
    },
    "Faltas": {
        "labels": ("Cometidas", "Recibidas"),
        "keys": ("fouls_committed", "fouls_received")
    }
}


def format_match_label(match):
    home_team = get_match_filter_value(match, "homeTeam")
    away_team = get_match_filter_value(match, "awayTeam")
    round_value = get_match_filter_value(match, "round")
    date_value = get_match_filter_value(match, "date")
    parts = []
    if round_value != "Sin datos":
        parts.append(f"J{round_value}")
    parts.append(f"{home_team} vs {away_team}")
    if date_value != "Sin datos":
        parts.append(date_value)
    return " · ".join(parts)


def build_season_event_details(matches, side="team"):
    """Aggregate team or opponent event categories and match occurrences."""
    if side not in ("team", "opponent"):
        raise ValueError("side must be 'team' or 'opponent'")

    totals = {
        category: [0] * len(details["keys"])
        for category, details in SEASON_EVENT_CATEGORIES.items()
    }
    match_rows = {category: [] for category in SEASON_EVENT_CATEGORIES}
    tracked_categories = {
        category: side == "team" or category in ("Goles", "Tiros", "Salidas")
        for category in SEASON_EVENT_CATEGORIES
    }

    for loaded_match in matches:
        match = loaded_match["data"]["match"].iloc[0]
        venue = match.get("venue")
        if venue not in ("home", "away"):
            venue = "home"
        team_stats = build_team_stats(loaded_match["data"]["events"], venue)
        opponent_venue = "away" if venue == "home" else "home"
        selected_venue = venue if side == "team" else opponent_venue
        selected_stats = team_stats[selected_venue]

        home_goals = match["homeGoals"]
        away_goals = match["awayGoals"]
        if side == "team":
            goals = (
                home_goals if venue == "home" else away_goals,
                away_goals if venue == "home" else home_goals
            )
        else:
            goals = (
                away_goals if venue == "home" else home_goals,
                home_goals if venue == "home" else away_goals
            )

        match_values = {
            "Goles": goals,
            "Tiros": (
                selected_stats["shots_target"],
                selected_stats["shots_off"]
            ),
            "Salidas": (
                selected_stats["buildout_success"],
                selected_stats["buildout_fail"]
            ),
            "Recuperaciones": (
                selected_stats["recovery_buildout"],
                selected_stats["recovery_build"],
                selected_stats["recovery_finish"]
            ),
            "Pérdidas": (
                selected_stats["loss_buildout"],
                selected_stats["loss_build"],
                selected_stats["loss_finish"]
            ),
            "Faltas": (
                selected_stats["fouls_committed"],
                selected_stats["fouls_received"]
            )
        }
        match_name = format_match_label(match)

        for category, values in match_values.items():
            if not tracked_categories[category]:
                continue
            labels = SEASON_EVENT_CATEGORIES[category]["labels"]
            for index, (label, value) in enumerate(zip(labels, values)):
                totals[category][index] += value
                if value:
                    match_rows[category].append({
                        "Partido": match_name,
                        "Evento": label,
                        "Cantidad": value
                    })

    categories = {}
    for category, details in SEASON_EVENT_CATEGORIES.items():
        labels = list(details["labels"])
        if side == "opponent" and category == "Goles":
            labels = ["Goles a favor del rival", "Goles en contra del rival"]
        categories[category] = {
            "labels": labels,
            "values": totals[category],
            "total": sum(totals[category]),
            "tracked": tracked_categories[category],
            "matches": pd.DataFrame(
                match_rows[category],
                columns=["Partido", "Evento", "Cantidad"]
            )
        }
    return categories
