import pandas as pd
import numpy as np
import db_conn as conn
import df_generators as df_gen

lol_csv_path = "extras/2024_LoL_esports_match_data_from_OraclesElixir.csv"
lol_df = df_gen.create_lol_dataframe(lol_csv_path)

date_filter = input("Digite uma data (YYYY-MM-DD): ")

cblol_df = df_gen.create_league_dataframe(lol_df, "CBLOL")

cblol_date_filtered_df = df_gen.filter_league_dataframe_by_date(cblol_df, date_filter)

cblol_player_analysis_df = df_gen.create_player_analysis_dataframe(cblol_date_filtered_df)

scores = [10, 8, 6, 4, 2]
columns_to_score = [
    "kda", "dpm", "vspm", "cspm", "wcpm", "wpm", "earned gpm", "geff", "geff team", "xpdiffat15", "csdiffat15", "golddiffat15", "kp"
]

top5_list = []

for column in columns_to_score:
    top5_df = cblol_player_analysis_df.nlargest(5, column)[["playername",column]]

    top5_dict = {
        "sector": column,
        "split" : cblol_player_analysis_df["split"].iloc[0],
        "patch" : cblol_player_analysis_df["patch"].iloc[0],
        "date" : cblol_player_analysis_df["date"].iloc[0],
        "playoffs" : int(cblol_player_analysis_df["playoffs"].iloc[0])
    }
    
    for rank, score in enumerate(scores):
        if rank < len(top5_df):
            playernames = top5_df.iloc[rank]["playername"]
            cblol_player_analysis_df.loc[
                cblol_player_analysis_df["playername"] == playernames, 
                "total_score"
            ] += score

            top5_dict[playernames] = {
                "value" : top5_df.iloc[rank][column],
                "score" : score
            }
            
    top5_list.append(top5_dict.copy())

conn.create_top5(top5_list)

cblol_player_analysis_df["total_score"] += (
    cblol_player_analysis_df["firstbloodkill"] * 5
    + cblol_player_analysis_df["firstbloodassist"] * 5
    - cblol_player_analysis_df["firstbloodvictim"] * 5
)

score_filter = ["playername", "total_score"]

cblol_player_score_list = cblol_player_analysis_df[score_filter].to_dict(orient="records")

for i in cblol_player_score_list:
    i["split"] = cblol_player_analysis_df["split"].iloc[0]
    i["date"] = cblol_player_analysis_df["date"].iloc[0]
    i["playoffs"] = int(cblol_player_analysis_df["playoffs"].iloc[0])

update_player = conn.update_player_record(cblol_player_score_list)

if not update_player:
    for i in cblol_player_score_list:
        i["date"] = [i["date"]]
    conn.create_player_record(cblol_player_score_list)

split = "Split 1"
playoff = 0

player_search = conn.get_player(split, playoff)

pl_top5_list = []

for i in player_search:
    top5_search = conn.get_top5(split, playoff)
    pl_top5_dict = {}
    top5s = []
    scr = []
    dates = []
    for j in top5_search:
        if i["playername"] in j:
            top5s.append(j["sector"])
            scr.append(j[i["playername"]]["score"])
            dates.append(j["date"])
    pl_top5_dict["player"] = i["playername"]
    pl_top5_dict["top 5s"] = top5s
    pl_top5_dict["scores"] = scr
    pl_top5_dict["dates"] = dates
    pl_top5_list.append(pl_top5_dict.copy())

print(pl_top5_list)
