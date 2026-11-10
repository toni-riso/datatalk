import json
import streamlit as st

from src.loaders.json_loader import load_match
from src.analysis.player_metrics import build_player_stats
from src.analysis.match_timeline import build_match_timeline
from src.analysis.match_report import (
    build_match_comparison,
    get_score_discrepancies
)
from src.analysis.season_metrics import (
    build_season_stats,
    filter_matches,
    get_match_filter_value
)
from src.analysis.team_metrics import build_team_stats


st.set_page_config(
    page_title="Data talk",
    layout="wide"
)

st.title("⚽ Data talk")


def render_season_dashboard(matches):
    all_seasons = sorted({
        get_match_filter_value(item["match"], "season")
        for item in matches
    })
    all_seasons_option = "Todas las temporadas"
    season_options = [all_seasons_option, *all_seasons]
    latest_season = all_seasons[-1] if all_seasons else all_seasons_option
    default_season = (
        st.session_state.get("season_filter", latest_season)
    )
    if default_season not in season_options:
        default_season = latest_season
    filters_changed = (
        st.session_state.get("season_filter") != default_season
    )
    st.session_state["season_filter"] = default_season
    selected_season = st.selectbox(
        "Temporada",
        season_options,
        index=season_options.index(default_season),
        key="season_filter"
    )

    season_matches = filter_matches(
        matches,
        season=(
            None
            if selected_season == all_seasons_option
            else selected_season
        )
    )
    all_competitions_option = "Todas las competiciones"
    competitions = sorted({
        get_match_filter_value(item["match"], "competition")
        for item in season_matches
    })
    competition_options = [all_competitions_option, *competitions]
    default_competition = st.session_state.get(
        "competition_filter",
        all_competitions_option
    )
    if default_competition not in competition_options:
        default_competition = all_competitions_option
    filters_changed = filters_changed or (
        st.session_state.get("competition_filter") != default_competition
    )
    st.session_state["competition_filter"] = default_competition
    if filters_changed:
        st.rerun()

    selected_competition = st.selectbox(
        "Competición",
        competition_options,
        index=competition_options.index(default_competition),
        key="competition_filter"
    )

    filtered_matches = filter_matches(
        matches,
        season=(
            None
            if selected_season == all_seasons_option
            else selected_season
        ),
        competition=(
            None
            if selected_competition == all_competitions_option
            else selected_competition
        )
    )
    if not filtered_matches:
        st.info("No hay partidos para los filtros seleccionados.")
        return

    season_stats = build_season_stats(filtered_matches)

    st.subheader("Temporada hasta hoy")
    st.caption(
        f"Acumulado de {season_stats['matches']} partidos cargados"
    )

    columns = st.columns(5)
    for column, (label, value) in zip(
        columns,
        (
            ("Partidos", season_stats["matches"]),
            (
                "Balance G-E-P",
                f"{season_stats['wins']}-{season_stats['draws']}-"
                f"{season_stats['losses']}"
            ),
            ("Puntos", season_stats["points"]),
            ("Goles a favor", season_stats["goals_for"]),
            ("Goles en contra", season_stats["goals_against"])
        )
    ):
        column.metric(label, value)

    columns = st.columns(5)
    for column, (label, value) in zip(
        columns,
        (
            ("Diferencia de goles", season_stats["goal_difference"]),
            (
                "Prom. goles a favor",
                round(season_stats["goals_for"] / season_stats["matches"], 2)
            ),
            (
                "Prom. goles en contra",
                round(
                    season_stats["goals_against"] / season_stats["matches"],
                    2
                )
            ),
            ("Porterías a cero", season_stats["clean_sheets"]),
            (
                "Puntos por partido",
                round(season_stats["points"] / season_stats["matches"], 2)
            )
        )
    ):
        column.metric(label, value)

    team_labels = {
        "Goles": "goals",
        "Tiros a puerta": "shots_target",
        "Tiros fuera": "shots_off",
        "Salidas exitosas": "buildout_success",
        "Salidas fallidas": "buildout_fail",
        "Regates completados": "dribble_ok",
        "Regates fallidos": "dribble_bad",
        "Recuperaciones": "recoveries",
        "Pérdidas": "losses",
        "Asistencias": "assists",
        "Córners": "corners_for",
        "Faltas cometidas": "fouls_committed",
        "Faltas recibidas": "fouls_received",
        "Amarillas": "yellow"
    }

    for heading, key in (
        ("Estadísticas acumuladas de nuestro equipo", "team"),
        ("Estadísticas acumuladas de los rivales", "opponent")
    ):
        with st.expander(heading, expanded=False):
            items = [
                (label, season_stats[key].get(metric, 0))
                for label, metric in team_labels.items()
            ]
            for start in range(0, len(items), 5):
                columns = st.columns(5)
                for column, (label, value) in zip(
                    columns,
                    items[start:start + 5]
                ):
                    column.metric(label, value)

    with st.expander("Estadísticas acumuladas de jugadores", expanded=False):
        st.caption(
            "Los minutos y acciones se suman; los porcentajes se recalculan "
            "sobre el total de partidos cargados. Haz clic en un encabezado "
            "para ordenar ascendente o descendentemente."
        )
        st.dataframe(
            season_stats["players"],
            use_container_width=True,
            hide_index=True
        )


def render_match_dashboard(data):
    match_df = data["match"]
    players_df = data["players"]
    events_df = data["events"]

    match = match_df.iloc[0]
    our_venue = match.get("venue")
    if our_venue not in ("home", "away"):
        st.warning(
            "El JSON no indica si nuestro equipo jugó como local o visitante. "
            "Para separar los eventos se asumirá que jugó como local."
        )
        our_venue = "home"

    player_stats = build_player_stats(
        players_df,
        events_df,
        match["currentSecond"]
    )
    team_stats = build_team_stats(events_df, our_venue)

    st.subheader(
        f"{match['homeTeam']} vs {match['awayTeam']}"
    )

    if our_venue == "home":
        home_goals = match["homeGoals"]
        away_goals = match["awayGoals"]
    else:
        home_goals = match["awayGoals"]
        away_goals = match["homeGoals"]

    discrepancies = get_score_discrepancies(
        team_stats,
        home_goals,
        away_goals
    )
    for discrepancy in discrepancies:
        st.warning(
            f"El marcador del {discrepancy['side'].lower()} indica "
            f"{discrepancy['score_goals']} goles, pero los eventos registran "
            f"{discrepancy['event_goals']}. Revisa los goles anotados."
        )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Goles local",
        home_goals
    )

    col2.metric(
        "Goles visitante",
        away_goals
    )

    col3.metric(
        "Jugadores",
        len(players_df)
    )

    col4.metric(
        "Eventos",
        len(events_df)
    )

    st.divider()

    st.subheader("Datos del partido")

    st.write(
        {
            "Competición": match["competition"],
            "Tipo": match["matchType"],
            "Temporada": match["season"],
            "Jornada": match["round"]
        }
    )

    st.subheader("Resumen comparativo")
    st.caption(
        "Los porcentajes muestran también el volumen usado para calcularlos. "
        "— indica que no hay intentos registrados."
    )
    st.dataframe(
        build_match_comparison(team_stats),
        use_container_width=True
    )

    st.divider()

    if team_stats["mismatched_team_labels"]:
        st.warning(
            f"{team_stats['mismatched_team_labels']} eventos tienen un campo "
            "`team` que no coincide con su tipo de acción. Para estos casos, "
            "la separación local/visitante se ha inferido del tipo de evento."
        )
    if team_stats["unassigned_events"]:
        st.warning(
            f"{team_stats['unassigned_events']} eventos no tienen un equipo "
            "local/visitante asignable y no se incluyen en estas estadísticas."
        )

    def render_side_stats(side, team_name, heading):
        st.markdown(f"#### {heading}: {team_name}")
        side_stats = team_stats[side]
        labels = {
            "Goles": side_stats["goals"],
            "Tiros a puerta": side_stats["shots_target"],
            "Tiros fuera": side_stats["shots_off"],
            "Salidas exitosas": side_stats["buildout_success"],
            "Salidas fallidas": side_stats["buildout_fail"],
            "Regates completados": side_stats["dribble_ok"],
            "Regates fallidos": side_stats["dribble_bad"],
            "Recuperaciones": side_stats["recoveries"],
            "Pérdidas": side_stats["losses"],
            "Asistencias": side_stats["assists"],
            "Córners": side_stats["corners_for"],
            "Faltas cometidas": side_stats["fouls_committed"],
            "Faltas recibidas": side_stats["fouls_received"],
            "Amarillas": side_stats["yellow"]
        }
        items = list(labels.items())
        for start in range(0, len(items), 5):
            columns = st.columns(5)
            for column, (label, value) in zip(
                columns,
                items[start:start + 5]
            ):
                column.metric(label, value)

    with st.expander("Estadísticas del equipo", expanded=False):
        render_side_stats("home", match["homeTeam"], "Local")
        render_side_stats("away", match["awayTeam"], "Visitante")

    with st.expander("Estadísticas de jugadores", expanded=False):
        st.caption(
            "Haz clic en el encabezado de una columna para ordenar "
            "ascendente o descendentemente."
        )
        st.dataframe(
            player_stats,
            use_container_width=True,
            hide_index=True
        )

    with st.expander("Cronología de eventos principales", expanded=False):
        timeline = build_match_timeline(events_df)
        if timeline.empty:
            st.info("Este partido no tiene eventos principales registrados.")
        else:
            st.dataframe(
                timeline,
                use_container_width=True,
                hide_index=True,
                height=min(620, 38 * (len(timeline) + 1))
            )
    
    #Ficha individual jugador
    # ==================================================
    # FICHA DEL JUGADOR
    # ==================================================

    with st.expander("Ficha individual del jugador", expanded=False):
        selected_player = st.selectbox(
            "Selecciona un jugador",
            player_stats["Jugador"].tolist()
        )

        player = player_stats[
            player_stats["Jugador"] == selected_player
        ].iloc[0]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Minutos", player["Min"])
        col1.metric("% Participación", player["% Part."])
        col2.metric("% Regate", player["% Regate"])
        col3.metric("Tiros", player["Tiros"])
        col3.metric("% Tiros Puerta", player["% Tiros Puerta"])
        col4.metric("Goles", player["Goles"])
        col4.metric("Acciones", player["Acciones"])

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ⚽ Juego ofensivo")
            st.write(f"**Regates OK:** {player['Regates OK']}")
            st.write(f"**Regates KO:** {player['Regates KO']}")
            st.write(f"**% Regate:** {player['% Regate']}")
            st.write(f"**Tiros:** {player['Tiros']}")
            st.write(f"**Tiros a Puerta:** {player['Tiros Puerta']}")
            st.write(f"**Tiros Fuera:** {player['Tiros Fuera']}")
            st.write(f"**% Tiros Puerta:** {player['% Tiros Puerta']}")
            st.write(f"**Goles:** {player['Goles']}")
            st.write(f"**Asistencias:** {player['Asistencias']}")

        with col2:
            st.markdown("### 🛡️ Juego defensivo")
            st.write(f"**Recuperaciones:** {player['Recuperaciones']}")
            st.write(f"**Pérdidas:** {player['Pérdidas']}")
            st.write(f"**Faltas Cometidas:** {player['Faltas Com.']}")
            st.write(f"**Faltas Recibidas:** {player['Faltas Rec.']}")
            st.write(f"**Amarillas:** {player['Amarillas']}")
            st.write(f"**Cambios:** {player['Cambios']}")
            st.write(f"**Acciones Totales:** {player['Acciones']}")



upload_key = "dashboard_match_files"
selection_key = "dashboard_match_selection"
season_option = "Temporada hasta hoy"
previous_uploads = st.session_state.get(upload_key, []) or []
previous_selection = st.session_state.get(
    selection_key,
    season_option
)
if previous_selection != season_option and not isinstance(
    previous_selection,
    str
):
    previous_selection = season_option

section_title = (
    f"Partidos cargados: {len(previous_uploads)}"
)
if previous_selection == season_option:
    selected_season = st.session_state.get("season_filter", "—")
    selected_competition = st.session_state.get("competition_filter", "—")
    section_title += (
        f" | Selección: {season_option}"
        f" | Temporada: {selected_season}"
        f" | Competición: {selected_competition}"
    )
else:
    section_title += f" | Selección: {previous_selection}"
selected_match = None
loaded_matches = []

with st.expander(
    section_title,
    expanded=not bool(previous_uploads)
):
    uploaded_files = st.file_uploader(
        "Carga uno o varios partidos (JSON)",
        type=["json"],
        accept_multiple_files=True,
        key=upload_key
    )
    uploaded_files = uploaded_files or []
    upload_errors = []

    for file_index, uploaded_file in enumerate(uploaded_files, start=1):
        try:
            uploaded_file.seek(0)
            data = load_match(uploaded_file)
            if data["match"].empty:
                raise ValueError("El fichero no contiene datos del partido.")

            match = data["match"].iloc[0]
            required_fields = (
                "date",
                "homeTeam",
                "awayTeam",
                "homeGoals",
                "awayGoals",
                "currentSecond",
                "competition",
                "matchType",
                "season",
                "round"
            )
            missing_fields = [
                field for field in required_fields
                if field not in match.index
            ]
            if missing_fields:
                raise ValueError(
                    "Faltan campos del partido: "
                    + ", ".join(missing_fields)
                )

            label = (
                f"{file_index}. {uploaded_file.name} | {match['date']} | "
                f"{match['homeTeam']} {match['homeGoals']}-"
                f"{match['awayGoals']} {match['awayTeam']}"
            )
            loaded_matches.append({
                "label": label,
                "filename": uploaded_file.name,
                "data": data,
                "match": match
            })
        except (
            json.JSONDecodeError,
            KeyError,
            TypeError,
            ValueError,
            UnicodeDecodeError
        ) as error:
            upload_errors.append(
                f"{uploaded_file.name}: {error}"
            )

    for error in upload_errors:
        st.error(f"No se pudo cargar el partido: {error}")

    if not loaded_matches:
        st.info("Carga uno o varios ficheros de partidos para empezar.")
    else:
        st.success(
            f"Partidos cargados correctamente: {len(loaded_matches)}"
        )
        st.dataframe(
            [
                {
                    "Archivo": item["filename"],
                    "Fecha": item["match"]["date"],
                    "Local": item["match"]["homeTeam"],
                    "Marcador": (
                        f"{item['match']['homeGoals']}-"
                        f"{item['match']['awayGoals']}"
                    ),
                    "Visitante": item["match"]["awayTeam"],
                    "Temporada": item["match"]["season"],
                    "Jornada": item["match"]["round"]
                }
                for item in loaded_matches
            ],
            use_container_width=True,
            hide_index=True
        )
        match_options = [
            season_option,
            *[item["label"] for item in loaded_matches]
        ]
        if st.session_state.get(selection_key) not in match_options:
            st.session_state[selection_key] = season_option

        selected_label = st.selectbox(
            "Partido para mostrar estadísticas",
            options=match_options,
            key=selection_key
        )
        if selected_label == season_option:
            selected_match = (season_option, loaded_matches)
        else:
            selected_match = next(
                (
                    item
                    for item in loaded_matches
                    if item["label"] == selected_label
                ),
                None
            )

if selected_match is not None:
    if isinstance(selected_match, tuple):
        render_season_dashboard(selected_match[1])
    else:
        render_match_dashboard(selected_match["data"])
