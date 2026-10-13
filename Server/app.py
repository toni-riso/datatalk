import streamlit as st
import plotly.graph_objects as go

from src.loaders.json_loader import load_match
from src.analysis.player_metrics import build_player_stats


st.set_page_config(
    page_title="Data talk",
    layout="wide"
)

st.title("⚽ Data talk")

uploaded_file = st.file_uploader(
    "Selecciona un fichero JSON",
    type=["json"]
)

if uploaded_file:

    import tempfile

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".json"
    ) as tmp:

        tmp.write(uploaded_file.read())

        file_path = tmp.name

    data = load_match(file_path)

    match_df = data["match"]
    players_df = data["players"]
    events_df = data["events"]

    match = match_df.iloc[0]

    player_stats = build_player_stats(
        players_df,
        events_df,
        match["currentSecond"],
        match["matchType"]
    )

    st.subheader(
        f"{match['homeTeam']} vs {match['awayTeam']}"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Goles",
        match["homeGoals"]
    )

    col2.metric(
        "Encajados",
        match["awayGoals"]
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

    st.divider()

    st.subheader("Estadísticas de jugadores")

    st.dataframe(
        player_stats,
        use_container_width=True,
        hide_index=True
    )
    #Tabla con los eventos 
    st.subheader("Eventos")

    st.dataframe(
        events_df,
        use_container_width=True,
        hide_index=True
    )
    
    #Barra lateral para elegir jugador
    #selected_player = st.sidebar.selectbox(
    #   "Jugador",
    #    player_stats["Jugador"]
    #)

    #Ficha individual jugador
    # ==================================================
    # FICHA DEL JUGADOR
    # ==================================================

    st.divider()

    st.subheader("👤 Ficha del jugador")

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

    col2.metric("% Pase", player["% Pase"])
    col2.metric("% Regate", player["% Regate"])

    col3.metric("Tiros", player["Tiros"])
    col3.metric("% Tiros Puerta", player["% Tiros Puerta"])

    col4.metric("Goles", player["Goles"])
    col4.metric("Acciones", player["Acciones"])

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### ⚽ Juego ofensivo")

        st.write(f"**Pases OK:** {player['Pases OK']}")
        st.write(f"**Pases KO:** {player['Pases KO']}")
        st.write(f"**% Pase:** {player['% Pase']}")

        st.write(f"**Regates OK:** {player['Regates OK']}")
        st.write(f"**Regates KO:** {player['Regates KO']}")
        st.write(f"**% Regate:** {player['% Regate']}")

        st.write(f"**Tiros:** {player['Tiros']}")
        st.write(f"**Tiros Puerta:** {player['Tiros Puerta']}")
        st.write(f"**Tiros Fuera:** {player['Tiros Fuera']}")
        st.write(f"**% Tiros Puerta:** {player['% Tiros Puerta']}")

        st.write(f"**Goles:** {player['Goles']}")

    with col2:

        st.markdown("### 🛡️ Juego defensivo")

        st.write(f"**Recuperaciones:** {player['Recuperaciones']}")
        st.write(f"**Pérdidas:** {player['Pérdidas']}")

        st.write(f"**Faltas Cometidas:** {player['Faltas Com.']}")
        st.write(f"**Faltas Recibidas:** {player['Faltas Rec.']}")

        st.write(f"**Amarillas:** {player['Amarillas']}")
        st.write(f"**Cambios:** {player['Cambios']}")

        st.write(f"**Acciones Totales:** {player['Acciones']}")
        st.write(f"**Acciones/Min:** {player['Acc/Min']}")
    
    #Gráfico Radar-1
    st.divider()

    st.subheader("📊 Radar del jugador")

    radar_categories = [
        "Pase",
        "Regate",
        "Finalización",
        "Defensa",
        "Gol"
    ]

    radar_values = [
        player["% Pase"],
        player["% Regate"],
        player["% Tiros Puerta"],
        min(player["Recuperaciones"] * 10, 100),
        min(player["Goles"] * 20, 100)
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=radar_values,
            theta=radar_categories,
            fill="toself",
            name=selected_player
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True
            )
        ),
        showlegend=False,
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )