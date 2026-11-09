# src/analysis/minutes.py

def calculate_minutes_played(player, match_duration_seconds):
    """
    Calcula los minutos jugados por un jugador a partir
    de sus stints.

    Parameters
    ----------
    player : pandas.Series
        Los valores de entrada/salida de los stints están en minutos.
    match_duration_seconds : int
        Duración transcurrida del partido, en segundos.

    Returns
    -------
    float
        Minutos jugados.
    """

    total_seconds = 0

    stints = player.get("stints", [])

    if not stints:
        return 0.0

    for stint in stints:

        start = stint.get("in", 0) * 60
        end_minute = stint.get("out")

        if end_minute is None:
            end = match_duration_seconds
        else:
            end = end_minute * 60

        total_seconds += max(0, end - start)

    return round(total_seconds / 60, 1)