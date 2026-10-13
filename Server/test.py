from src.loaders.json_loader import load_match
from src.analysis.player_metrics import build_player_stats

# Ruta a tu JSON exportado
FILE = "data/ejemplo2.json"

data = load_match(FILE)

match_df = data["match"]
players_df = data["players"]
events_df = data["events"]

player_stats = build_player_stats(
    players_df,
    events_df,
    match_df.iloc[0]["currentSecond"],
    match_df.iloc[0]["matchType"]
)
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_rows", None)
              
print()
print("=== DATOS PARTIDO ===")
print(match_df)
print()

print("=== ESTADÍSTICAS JUGADORES ===")
print(player_stats)
print()