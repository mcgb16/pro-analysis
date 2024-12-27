import pandas as pd

lol_csv_path = "extras/2024_LoL_esports_match_data_from_OraclesElixir.csv"

lol_df = pd.read_csv(lol_csv_path , sep="," , dtype={'url': str})

cblol_df = lol_df[lol_df["league"] == "CBLOL"]
cblol_df['geff'] = cblol_df['dpm'] / cblol_df['earned gpm']
cblol_df['geff team'] = cblol_df['damageshare'] / cblol_df['earnedgoldshare']

columns_player_analysis = [
    "playername",
    "position",
    "dpm",
    "earned gpm",
    "geff",
    "wcpm",
    "wpm",
    "vspm",
    "cspm",
    "golddiffat15",
    "csdiffat15",
    "xpdiffat15",
    "firstbloodkill",
    "firstbloodassist",
    "firstbloodvictim",
    "damageshare",
    "earnedgoldshare",
    "geff team"
]

player_analysis_agg_dict =     {
        "position": "first",
        "dpm": "mean",
        "earned gpm": "mean",
        "geff": "mean",
        "wcpm": "mean",
        "wpm": "mean",
        "vspm": "mean",
        "cspm": "mean",
        "golddiffat15": "mean",
        "csdiffat15": "mean",
        "xpdiffat15": "mean",
        "firstbloodkill": "mean",
        "firstbloodassist": "mean",
        "firstbloodvictim": "mean",
        "damageshare": "mean",
        "earnedgoldshare": "mean",
        "geff team": "mean"
    }

cblol_player_analysis_df = cblol_df[columns_player_analysis].copy()

cblol_player_avg_df = cblol_player_analysis_df.groupby('playername').agg(player_analysis_agg_dict).reset_index()

print(cblol_player_avg_df.head())