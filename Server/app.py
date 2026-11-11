import json
import streamlit as st
import plotly.graph_objects as go

from src.loaders.json_loader import load_match
from src.analysis.player_metrics import build_player_stats
from src.analysis.player_event_details import (
    build_player_event_details,
    build_player_recovery_counts
)
from src.analysis.match_timeline import build_match_timeline
from src.analysis.team_event_details import (
    build_event_chart_data,
    build_team_event_details
)
from src.analysis.match_report import (
    build_match_comparison,
    get_score_discrepancies
)
from src.analysis.season_metrics import (
    build_season_stats,
    filter_matches,
    get_match_filter_value
)
from src.analysis.season_event_details import build_season_event_details
from src.analysis.season_player_details import build_season_player_details
from src.analysis.team_metrics import build_team_stats


st.set_page_config(
    page_title="Data talk",
    layout="wide"
)

st.title("⚽ Data talk")


def build_donut_chart(title, labels, values, total):
    chart_labels = labels if total else ["Sin datos"]
    chart_values = values if total else [1]
    color_by_label = {
        "A puerta": "#2e8b57",
        "A puerta (incl. goles)": "#2e8b57",
        "Tiros a puerta": "#2e8b57",
        "Fuera": "#e07a5f",
        "Tiros fuera": "#e07a5f",
        "Completados": "#2e8b57",
        "Fallidos": "#e07a5f",
        "Exitosas": "#2e8b57",
        "Fallidas": "#e07a5f",
        "Goles a favor": "#2e8b57",
        "Goles en contra": "#e07a5f",
        "Goles a favor del rival": "#2e8b57",
        "Goles en contra del rival": "#e07a5f",
        "Cometidas": "#e07a5f",
        "Recibidas": "#4c78a8",
        "Salida": "#4c78a8",
        "Construcción": "#f2b134",
        "Finalización": "#7a5195",
        "Sin especificar": "#9e9e9e",
        "Sin datos": "#e0e0e0"
    }
    chart = go.Figure(data=[go.Pie(
        labels=chart_labels,
        values=chart_values,
        hole=0.68,
        sort=False,
        textinfo="label+value" if total else "none",
        hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
        marker={
            "colors": [
                color_by_label.get(label, "#9e9e9e")
                for label in chart_labels
            ]
        }
    )])
    chart.update_layout(
        title=title,
        height=300,
        margin={"l": 10, "r": 10, "t": 45, "b": 35},
        showlegend=bool(total),
        legend={"orientation": "h", "y": -0.08},
        annotations=[{
            "text": f"<b>{total}</b><br>Total",
            "x": 0.5,
            "y": 0.5,
            "showarrow": False,
            "font": {"size": 20}
        }]
    )
    return chart


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

    for heading, key in (
        ("Estadísticas acumuladas de nuestro equipo", "team"),
        ("Estadísticas acumuladas de los rivales", "opponent")
    ):
        with st.expander(heading, expanded=False):
            if key in ("team", "opponent"):
                season_event_details = build_season_event_details(
                    filtered_matches,
                    side=key
                )
                if key == "team":
                    st.caption(
                        "Cada tabla indica los partidos donde se registró "
                        "cada tipo de evento y su cantidad."
                    )
                else:
                    st.caption(
                        "Goles, tiros y salidas del rival se muestran con "
                        "detalle por partido. Recuperaciones, pérdidas y "
                        "faltas del rival no se registran en los eventos."
                    )
                category_names = list(season_event_details)
                for start in range(0, len(category_names), 2):
                    columns = st.columns(2)
                    for column, category in zip(
                        columns,
                        category_names[start:start + 2]
                    ):
                        category_data = season_event_details[category]
                        with column:
                            if not category_data["tracked"]:
                                st.info(
                                    f"{category}: este dato no se registra "
                                    "para el rival."
                                )
                                continue
                            st.plotly_chart(
                                build_donut_chart(
                                    category,
                                    category_data["labels"],
                                    category_data["values"],
                                    category_data["total"]
                                ),
                                use_container_width=True,
                                config={"displayModeBar": False}
                            )
                            match_count = len(category_data["matches"])
                            show_details = st.checkbox(
                                f"Ver detalle por partido ({match_count})",
                                key=f"season_details_{key}_{category}"
                            )
                            if show_details:
                                if category_data["matches"].empty:
                                    st.caption(
                                        "No hay eventos registrados en estos "
                                        "partidos."
                                    )
                                else:
                                    st.dataframe(
                                        category_data["matches"],
                                        use_container_width=True,
                                        hide_index=True,
                                        height=260
                                    )

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

    season_players = season_stats["players"]
    if not season_players.empty:
        with st.expander("Ficha individual del jugador", expanded=False):
            player_options = list(range(len(season_players)))
            selected_player_index = st.selectbox(
                "Selecciona un jugador",
                player_options,
                format_func=lambda index: (
                    f"#{season_players.iloc[index]['Dorsal']} · "
                    f"{season_players.iloc[index]['Jugador']} "
                    f"({season_players.iloc[index]['Posición']})"
                ),
                key="season_player_profile"
            )
            player = season_players.iloc[selected_player_index]
            player_details = build_season_player_details(
                filtered_matches,
                player["Dorsal"],
                player["Jugador"]
            )
            played_fraction = min(
                max(float(player["% Part."]) / 100, 0),
                1
            )

            st.markdown(
                f"### #{player['Dorsal']} · {player['Jugador']} "
                f"— {player['Posición']}"
            )
            st.caption(
                f"{player['Titularidades']} titularidades · "
                f"{player['Convocatorias']} convocatorias"
            )
            st.progress(played_fraction, text="Participación en la temporada")
            st.caption(
                f"{player['Min']:.1f} minutos · "
                f"{player['% Part.']}% del tiempo total disputado"
            )

            summary_columns = st.columns(6)
            for column, label, value in zip(
                summary_columns,
                (
                    "Partidos",
                    "Goles",
                    "Asistencias",
                    "Tiros",
                    "Regates",
                    "Acciones"
                ),
                (
                    player["Partidos"],
                    player["Goles"],
                    player["Asistencias"],
                    player["Tiros"],
                    player["Regates OK"] + player["Regates KO"],
                    player["Acciones"]
                )
            ):
                column.metric(label, value)

            st.markdown("### ⚽ Ataque")
            shots_column, dribbles_column = st.columns(2)
            shot_values = [player["Tiros Puerta"], player["Tiros Fuera"]]
            shot_total = sum(shot_values)
            with shots_column:
                st.plotly_chart(
                    build_donut_chart(
                        "Tiros",
                        ["A puerta", "Fuera"],
                        shot_values,
                        shot_total
                    ),
                    use_container_width=True,
                    config={"displayModeBar": False}
                )
                st.caption(
                    f"Precisión a puerta: {player['% Tiros Puerta']}%"
                    if shot_total
                    else "Sin intentos de tiro."
                )
            with dribbles_column:
                dribble_values = [
                    player["Regates OK"],
                    player["Regates KO"]
                ]
                dribble_total = sum(dribble_values)
                st.plotly_chart(
                    build_donut_chart(
                        "Regates",
                        ["Completados", "Fallidos"],
                        dribble_values,
                        dribble_total
                    ),
                    use_container_width=True,
                    config={"displayModeBar": False}
                )
                st.caption(
                    f"Éxito en regate: {player['% Regate']}%"
                    if dribble_total
                    else "Sin intentos de regate."
                )

            st.markdown("### 🛡️ Defensa")
            recovery_column, loss_column = st.columns(2)
            recovery_values = player_details["recoveries"]
            recovery_labels = [
                "Salida",
                "Construcción",
                "Finalización",
                "Sin especificar"
            ]
            with recovery_column:
                st.plotly_chart(
                    build_donut_chart(
                        "Recuperaciones",
                        recovery_labels,
                        recovery_values,
                        sum(recovery_values)
                    ),
                    use_container_width=True,
                    config={"displayModeBar": False}
                )
            with loss_column:
                loss_values = player_details["losses"]
                st.plotly_chart(
                    build_donut_chart(
                        "Pérdidas",
                        recovery_labels,
                        loss_values,
                        sum(loss_values)
                    ),
                    use_container_width=True,
                    config={"displayModeBar": False}
                )

            defensive_columns = st.columns(4)
            for column, label, value in zip(
                defensive_columns,
                ("Faltas cometidas", "Faltas recibidas", "Amarillas", "Cambios"),
                (
                    player["Faltas Com."],
                    player["Faltas Rec."],
                    player["Amarillas"],
                    player["Cambios"]
                )
            ):
                column.metric(label, value)

            timeline = player_details["timeline"]
            show_timeline = st.checkbox(
                f"Ver cronología por partido ({len(timeline)} eventos)",
                key=f"season_player_timeline_{player['Dorsal']}_{player['Jugador']}"
            )
            if show_timeline:
                if timeline.empty:
                    st.info("Este jugador no tiene eventos registrados.")
                else:
                    st.dataframe(
                        timeline,
                        use_container_width=True,
                        hide_index=True,
                        height=320
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

    home_goals = match["homeGoals"]
    away_goals = match["awayGoals"]

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
        "— indica que no hay intentos registrados o que ese dato no se "
        "recoge para ese equipo."
    )
    comparison = build_match_comparison(
        team_stats,
        match["homeTeam"],
        match["awayTeam"]
    )
    st.dataframe(comparison, use_container_width=True)

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
        side_goals = team_stats[side]["goals"]
        st.markdown(
            f"#### {heading}: {team_name} · {side_goals} goles"
        )
        side_stats = team_stats[side]
        labels = {
            "Tiros a puerta": side_stats["shots_target"],
            "Tiros fuera": side_stats["shots_off"],
            "Salidas exitosas": side_stats["buildout_success"],
            "Salidas fallidas": side_stats["buildout_fail"],
            "Recuperaciones": side_stats["recoveries"],
            "Pérdidas": side_stats["losses"],
            "Córners": side_stats["corners_for"]
        }
        items = list(labels.items())
        columns = st.columns(len(items))
        for column, (label, value) in zip(columns, items):
            column.metric(label, value)

        details = build_team_event_details(
            events_df,
            side,
            our_venue
        )
        for title, key in (
            ("Tiros", "shots"),
            ("Salidas", "buildouts"),
            ("Recuperaciones", "recoveries")
        ):
            event_table = details[key]
            if key == "recoveries" and side != our_venue:
                st.markdown(f"**{title}**")
                st.caption(
                    "El detalle de recuperaciones solo se registra "
                    "para nuestro equipo."
                )
                continue

            labels_for_chart, values_for_chart, total = (
                build_event_chart_data(event_table, key)
            )
            chart_column, events_column = st.columns([1, 1.4])
            with chart_column:
                st.plotly_chart(
                    build_donut_chart(
                        title,
                        labels_for_chart,
                        values_for_chart,
                        total
                    ),
                    use_container_width=True,
                    config={"displayModeBar": False}
                )

            with events_column:
                st.markdown(f"**Detalle de {title.lower()}**")
                if event_table.empty:
                    st.caption("No hay eventos registrados.")
                    continue
                st.dataframe(
                    event_table,
                    use_container_width=True,
                    hide_index=True
                )

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
        player_options = list(range(len(player_stats)))
        selected_player = st.selectbox(
            "Selecciona un jugador",
            player_options,
            format_func=lambda index: (
                f"#{player_stats.iloc[index]['Dorsal']} · "
                f"{player_stats.iloc[index]['Jugador']} "
                f"({player_stats.iloc[index]['Posición']})"
            )
        )
        player = player_stats.iloc[selected_player]
        matching_players = players_df[
            (players_df["dorsal"] == player["Dorsal"]) &
            (players_df["name"] == player["Jugador"])
        ]
        player_id = matching_players.iloc[0]["id"]
        played_fraction = min(max(float(player["% Part."]) / 100, 0), 1)

        st.markdown(
            f"### #{player['Dorsal']} · {player['Jugador']} "
            f"— {player['Posición']}"
        )
        st.caption(
            "Titular" if player["Titular"] else "Suplente"
        )
        st.progress(played_fraction, text="Participación en el partido")
        st.caption(
            f"{player['Min']} min de {round(match['currentSecond'] / 60, 1)} "
            f"({player['% Part.']}%)"
        )

        summary_columns = st.columns(5)
        for column, label, value in zip(
            summary_columns,
            ("Goles", "Asistencias", "Tiros", "Regates", "Acciones"),
            (
                player["Goles"],
                player["Asistencias"],
                player["Tiros"],
                player["Regates OK"] + player["Regates KO"],
                player["Acciones"]
            )
        ):
            column.metric(label, value)

        st.markdown("### ⚽ Ataque")
        shots_column, dribbles_column = st.columns(2)
        shot_total = player["Tiros Puerta"] + player["Tiros Fuera"]
        shot_labels = ["A puerta", "Fuera"]
        shot_values = [player["Tiros Puerta"], player["Tiros Fuera"]]
        with shots_column:
            st.plotly_chart(
                build_donut_chart(
                    "Tiros",
                    shot_labels,
                    shot_values,
                    shot_total
                ),
                use_container_width=True,
                config={"displayModeBar": False}
            )
            st.caption(
                f"Precisión a puerta: {player['% Tiros Puerta']}%"
                if shot_total
                else "Sin intentos de tiro."
            )
        with dribbles_column:
            dribble_values = [
                player["Regates OK"],
                player["Regates KO"]
            ]
            dribble_total = sum(dribble_values)
            st.plotly_chart(
                build_donut_chart(
                    "Regates",
                    ["Completados", "Fallidos"],
                    dribble_values,
                    dribble_total
                ),
                use_container_width=True,
                config={"displayModeBar": False}
            )
            st.caption(
                f"Éxito en regate: {player['% Regate']}%"
                if dribble_total
                else "Sin intentos de regate."
            )

        st.markdown("### 🛡️ Defensa")
        recovery_values = build_player_recovery_counts(
            events_df,
            player_id,
            (
                "recovery_buildout",
                "recovery_build",
                "recovery_finish",
                "recovery"
            )
        )
        if sum(recovery_values[:3]) == 0:
            recovery_values[:3] = [0, 0, 0]
        else:
            recovery_values[3] = 0
        loss_values = build_player_recovery_counts(
            events_df,
            player_id,
            (
                "loss_buildout",
                "loss_build",
                "loss_finish",
                "loss"
            )
        )
        if sum(loss_values[:3]) == 0:
            loss_values[:3] = [0, 0, 0]
        else:
            loss_values[3] = 0

        recovery_column, loss_column = st.columns(2)
        with recovery_column:
            st.plotly_chart(
                build_donut_chart(
                    "Recuperaciones",
                    ["Salida", "Construcción", "Finalización", "Sin especificar"],
                    recovery_values,
                    sum(recovery_values)
                ),
                use_container_width=True,
                config={"displayModeBar": False}
            )
        with loss_column:
            st.plotly_chart(
                build_donut_chart(
                    "Pérdidas",
                    ["Salida", "Construcción", "Finalización", "Sin especificar"],
                    loss_values,
                    sum(loss_values)
                ),
                use_container_width=True,
                config={"displayModeBar": False}
            )

        defensive_columns = st.columns(4)
        for column, label, value in zip(
            defensive_columns,
            ("Faltas cometidas", "Faltas recibidas", "Amarillas", "Cambios"),
            (
                player["Faltas Com."],
                player["Faltas Rec."],
                player["Amarillas"],
                player["Cambios"]
            )
        ):
            column.metric(label, value)

        player_timeline = build_player_event_details(events_df, player_id)
        show_player_timeline = st.checkbox(
            f"Ver cronología del jugador ({len(player_timeline)} eventos)",
            key=f"player_timeline_{player_id}"
        )
        if show_player_timeline:
            if player_timeline.empty:
                st.info("Este jugador no tiene eventos registrados.")
            else:
                st.dataframe(
                    player_timeline,
                    use_container_width=True,
                    hide_index=True,
                    height=320
                )



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
