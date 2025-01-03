import pandas as pd
import numpy as np
import db_conn as conn
import df_generators as df_gen
import analysis

lol_csv_path = "extras/2024_LoL_esports_match_data_from_OraclesElixir.csv"
lol_df = df_gen.create_lol_dataframe(lol_csv_path)

date_filter = input("Digite uma data (YYYY-MM-DD): ")

cblol_df = df_gen.create_league_dataframe(lol_df, "CBLOL")

cblol_date_filtered_df = df_gen.filter_league_dataframe_by_date(cblol_df, date_filter)

cblol_player_analysis_df = df_gen.create_player_analysis_dataframe(cblol_date_filtered_df)

cblol_top5_list = analysis.create_top5_dict_list(cblol_player_analysis_df)

first_blood_score_insert = analysis.insert_first_blood_score(cblol_player_analysis_df)

cblol_player_score_list = analysis.create_plscore_dict_list(cblol_player_analysis_df)

conn.create_top5(cblol_top5_list)

update_player = conn.update_player_record(cblol_player_score_list)

if not update_player:
    for i in cblol_player_score_list:
        i["date"] = [i["date"]]
    conn.create_player_record(cblol_player_score_list)

split = "Split 1"
playoff = 0

pl_top5_list = analysis.create_pltop5_dict_list(split, playoff)
