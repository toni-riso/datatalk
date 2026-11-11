import pandas as pd

from src.analysis.match_analysis import analyze_match


PLAYER_COUNT_COLUMNS = (
    "Regates OK",
    "Regates KO",
    "Tiros",
    "Tiros Puerta",
    "Tiros Fuera",
    "Goles",
    "Asistencias",
    "Recuperaciones",
    "Pérdidas",
    "Faltas Com.",
    "Faltas Rec.",
    "Amarillas",
    "Cambios",
    "Acciones"
)


def get_match_filter_value(match, field):
    value = match.get(field)
    if pd.isna(value):
        return "Sin datos"
    return str(value)


def filter_matches(matches, season=None, competition=None):
    """Return only uploaded matches matching the selected filters."""
    filtered_matches = []
    for loaded_match in matches:
        match = loaded_match["match"]
        if season is not None and get_match_filter_value(
            match,
            "season"
        ) != season:
            continue
        if competition is not None and get_match_filter_value(
            match,
            "competition"
        ) != competition:
            continue
        filtered_matches.append(loaded_match)
    return filtered_matches


def build_season_stats(matches, match_analyses=None):
    """Aggregate match, team, and player metrics across loaded matches."""
    if match_analyses is not None and len(match_analyses) != len(matches):
        raise ValueError("match_analyses must align with matches")

    summary = {
        "matches": len(matches),
        "wins": 0,
        "draws": 0,
        "losses": 0,
        "points": 0,
        "goals_for": 0,
        "goals_against": 0,
        "goal_difference": 0,
        "clean_sheets": 0,
        "team": {},
        "opponent": {},
        "players": pd.DataFrame()
    }
    player_totals = {}
    total_match_seconds = 0

    for index, loaded_match in enumerate(matches):
        data = loaded_match["data"]
        match = data["match"].iloc[0]
        venue = match.get("venue")
        if venue not in ("home", "away"):
            venue = "home"

        if venue == "home":
            our_goals = match["homeGoals"]
            opponent_goals = match["awayGoals"]
        else:
            our_goals = match["awayGoals"]
            opponent_goals = match["homeGoals"]
        summary["goals_for"] += our_goals
        summary["goals_against"] += opponent_goals
        if opponent_goals == 0:
            summary["clean_sheets"] += 1
        if our_goals > opponent_goals:
            summary["wins"] += 1
        elif our_goals == opponent_goals:
            summary["draws"] += 1
        else:
            summary["losses"] += 1

        match_analysis = (
            match_analyses[index]
            if match_analyses is not None
            else analyze_match(data)
        )
        team_stats = match_analysis["team_stats"]
        our_stats = team_stats[venue]
        opponent_venue = "away" if venue == "home" else "home"
        opponent_stats = team_stats[opponent_venue]
        for key, value in our_stats.items():
            summary["team"][key] = summary["team"].get(key, 0) + value
        for key, value in opponent_stats.items():
            summary["opponent"][key] = (
                summary["opponent"].get(key, 0) + value
            )

        match_duration = match["currentSecond"]
        total_match_seconds += match_duration
        player_stats = match_analysis["player_stats"]
        for _, player in player_stats.iterrows():
            key = (player["Dorsal"], player["Jugador"])
            totals = player_totals.setdefault(
                key,
                {
                    "Dorsal": player["Dorsal"],
                    "Jugador": player["Jugador"],
                    "Posición": player["Posición"],
                    "Partidos": 0,
                    "Convocatorias": 0,
                    "Titularidades": 0,
                    "Min": 0.0,
                    **{column: 0 for column in PLAYER_COUNT_COLUMNS}
                }
            )
            totals["Convocatorias"] += 1
            totals["Partidos"] += int(player["Min"] > 0)
            totals["Titularidades"] += int(bool(player["Titular"]))
            totals["Min"] += player["Min"]
            for column in PLAYER_COUNT_COLUMNS:
                totals[column] += player[column]

    summary["points"] = summary["wins"] * 3 + summary["draws"]
    summary["goal_difference"] = (
        summary["goals_for"] - summary["goals_against"]
    )

    if player_totals:
        players = pd.DataFrame(player_totals.values())
        players["% Part."] = (
            (players["Min"] * 60 / total_match_seconds * 100).round(1)
            if total_match_seconds > 0
            else 0.0
        )
        dribble_attempts = players["Regates OK"] + players["Regates KO"]
        players["% Regate"] = (
            players["Regates OK"].div(dribble_attempts).fillna(0).mul(100)
        ).round(1)
        players["% Tiros Puerta"] = (
            players["Tiros Puerta"].div(players["Tiros"]).fillna(0).mul(100)
        ).round(1)
        players = players[
            [
                "Dorsal",
                "Jugador",
                "Posición",
                "Partidos",
                "Convocatorias",
                "Titularidades",
                "Min",
                "% Part.",
                "Regates OK",
                "Regates KO",
                "% Regate",
                "Tiros",
                "Tiros Puerta",
                "Tiros Fuera",
                "% Tiros Puerta",
                "Goles",
                "Asistencias",
                "Recuperaciones",
                "Pérdidas",
                "Faltas Com.",
                "Faltas Rec.",
                "Amarillas",
                "Cambios",
                "Acciones"
            ]
        ].sort_values(
            by=["Min", "Acciones"],
            ascending=False
        ).reset_index(drop=True)
        summary["players"] = players

    return summary
