import pandas as pd


def _percentage(numerator, denominator):
    if denominator == 0:
        return "—"
    percentage = round(numerator / denominator * 100, 1)
    return f"{percentage}% ({numerator}/{denominator})"


def build_match_comparison(team_stats, home_team=None, away_team=None):
    """Create a team-by-metric comparison grouped into stat sections."""
    rows = []
    for label, key, team_name in (
        ("Local", "home", home_team),
        ("Visitante", "away", away_team)
    ):
        if team_name:
            label = f"{label} ({team_name})"
        stats = team_stats[key]
        tracked_for_side = key == team_stats["our_venue"]
        total_shots = stats["shots_target"] + stats["shots_off"]
        buildout_attempts = (
            stats["buildout_success"] + stats["buildout_fail"]
        )
        rows.append({
            "Equipo": label,
            ("Tiros y córners", "Goles"): stats["goals"],
            ("Tiros y córners", "Tiros a puerta"): stats["shots_target"],
            ("Tiros y córners", "Tiros fuera"): stats["shots_off"],
            ("Tiros y córners", "Tiros totales"): total_shots,
            ("Tiros y córners", "Precisión de tiro"): _percentage(
                stats["shots_target"], total_shots
            ),
            ("Tiros y córners", "Córners"): stats["corners_for"],
            ("Salidas", "Salidas exitosas"): stats["buildout_success"],
            ("Salidas", "Salidas fallidas"): stats["buildout_fail"],
            ("Salidas", "Éxito en salida"): _percentage(
                stats["buildout_success"], buildout_attempts
            ),
            ("Recuperaciones", "Salida"): (
                stats["recovery_buildout"] if tracked_for_side else "—"
            ),
            ("Recuperaciones", "Construcción"): (
                stats["recovery_build"] if tracked_for_side else "—"
            ),
            ("Recuperaciones", "Finalización"): (
                stats["recovery_finish"] if tracked_for_side else "—"
            ),
            ("Pérdidas", "Salida"): (
                stats["loss_buildout"] if tracked_for_side else "—"
            ),
            ("Pérdidas", "Construcción"): (
                stats["loss_build"] if tracked_for_side else "—"
            ),
            ("Pérdidas", "Finalización"): (
                stats["loss_finish"] if tracked_for_side else "—"
            )
        })

    comparison = pd.DataFrame(rows).set_index("Equipo")
    comparison.columns = pd.MultiIndex.from_tuples(
        comparison.columns,
        names=("Sección", "Estadística")
    )
    return comparison


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
