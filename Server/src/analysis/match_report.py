import pandas as pd


def _percentage(numerator, denominator):
    if denominator == 0:
        return "—"
    percentage = round(numerator / denominator * 100, 1)
    return f"{percentage}% ({numerator}/{denominator})"


def build_match_comparison(team_stats):
    """Create comparable match metrics for the actual home and away sides."""
    rows = []
    for label, key in (("Local", "home"), ("Visitante", "away")):
        stats = team_stats[key]
        total_shots = stats["shots_target"] + stats["shots_off"]
        buildout_attempts = (
            stats["buildout_success"] + stats["buildout_fail"]
        )
        rows.append({
            "Equipo": label,
            "Goles": stats["goals"],
            "Tiros a puerta": stats["shots_target"],
            "Tiros fuera": stats["shots_off"],
            "Tiros totales": total_shots,
            "Precisión de tiro": _percentage(
                stats["shots_target"],
                total_shots
            ),
            "Conversión de tiro": _percentage(
                stats["goals"],
                total_shots
            ),
            "Salidas exitosas": stats["buildout_success"],
            "Salidas fallidas": stats["buildout_fail"],
            "Éxito en salida": _percentage(
                stats["buildout_success"],
                buildout_attempts
            )
        })

    return pd.DataFrame(rows).set_index("Equipo").transpose()


def get_score_discrepancies(team_stats, home_score, away_score):
    """Return sides where event goals do not match the recorded scoreboard."""
    discrepancies = []
    for side, label, score in (
        ("home", "Local", home_score),
        ("away", "Visitante", away_score)
    ):
        event_goals = team_stats[side]["goals"]
        if event_goals != score:
            discrepancies.append({
                "side": label,
                "score_goals": score,
                "event_goals": event_goals
            })
    return discrepancies
