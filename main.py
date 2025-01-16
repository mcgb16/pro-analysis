import db_conn as conn
import df_generators as df_gen
import plot_creation as plt
import analysis

lol_csv_path = "extras/2024_LoL_esports_match_data_from_OraclesElixir.csv"

date = input("Digite uma data (YYYY-MM-DD): ")
date_filter = []
date_filter.append(date)

split = "Split 1"


lol_df = df_gen.create_lol_dataframe(lol_csv_path)

cblol_df = df_gen.create_league_dataframe(lol_df, "CBLOL")

cblol_date_filtered_df = df_gen.filter_league_dataframe_by_date(cblol_df, date_filter)

cblol_player_analysis_df = df_gen.create_player_analysis_dataframe(cblol_date_filtered_df)

cblol_top10_list = analysis.create_top10_dict_list(cblol_player_analysis_df)

first_blood_score_insert = analysis.insert_first_blood_score(cblol_player_analysis_df)

cblol_player_analysis_list = analysis.create_player_analysis_dict_list(cblol_player_analysis_df)

conn.create_top10(cblol_top10_list)
conn.create_info_player_record(cblol_player_analysis_list)

player_info_list = conn.get_info_player(split)
player_info_df = df_gen.create_dataframe_from_list(player_info_list)

player_info_df.to_csv("extras/csv/stage_player_info.csv", index=False)
