import pandas as pd
import numpy as np

lol_csv_path = "extras/2024_LoL_esports_match_data_from_OraclesElixir.csv"

lol_df = pd.read_csv(lol_csv_path , sep="," , dtype={'url': str})

date_filter = input("Digite uma data (YYYY-MM-DD): ")

cblol_df = lol_df[lol_df["league"] == "CBLOL"].copy()
cblol_df['geff'] = cblol_df['dpm'] / cblol_df['earned gpm']
cblol_df['geff team'] = cblol_df['damageshare'] / cblol_df['earnedgoldshare']
cblol_df['kp'] = (cblol_df["kills"] + cblol_df["assists"]) / cblol_df["teamkills"]
cblol_df['kda'] = (cblol_df["kills"] + cblol_df["assists"]) / cblol_df["deaths"].replace(0, np.nan)
cblol_df['kda'] = cblol_df['kda'].fillna(cblol_df["kills"] + cblol_df["assists"])

cblol_filtered_df = cblol_df[cblol_df["date"].str.contains(date_filter)]


columns_player_analysis = [
    "playername",
    "position",
    "kda",
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
    "geff team",
    "kp"
]

player_analysis_agg_dict = {
        "position": "first",
        "kda": "mean",
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
        "firstbloodkill": "sum",
        "firstbloodassist": "sum",
        "firstbloodvictim": "sum",
        "damageshare": "mean",
        "earnedgoldshare": "mean",
        "geff team": "mean",
        "kp" : "mean"
    }

cblol_player_analysis_df = cblol_filtered_df[columns_player_analysis].copy()
cblol_player_avg_df = cblol_player_analysis_df.groupby('playername').agg(player_analysis_agg_dict).reset_index()

scores = [10, 8, 6, 4, 2]
columns_to_score = [
    "kda", "dpm", "vspm", "cspm", "wcpm", "wpm", "earned gpm", "geff", "geff team", "xpdiffat15", "csdiffat15", "golddiffat15", "kp"
]

cblol_player_avg_df["total_score"] = 0

for column in columns_to_score:
    top5_df = cblol_player_avg_df.nlargest(5, column)

    print(column)
    print(top5_df)
    print("######################")
    
    for rank, score in enumerate(scores):
        if rank < len(top5_df):
            playernames = top5_df.iloc[rank]["playername"]
            cblol_player_avg_df.loc[
                cblol_player_avg_df["playername"] == playernames, 
                "total_score"
            ] += score

cblol_player_avg_df["total_score"] += (
    cblol_player_avg_df["firstbloodkill"] * 5
    + cblol_player_avg_df["firstbloodassist"] * 5
    - cblol_player_avg_df["firstbloodvictim"] * 5
)

print(cblol_player_avg_df[["playername", "total_score"]].sort_values(by="total_score", ascending=False))

# print(cblol_player_avg_df.head())