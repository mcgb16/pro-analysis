import db_conn as conn
import df_generators as df_gen
import analysis

lol_csv_path = "extras/2024_LoL_esports_match_data_from_OraclesElixir.csv"

date_filter_list = [
    ["2024-06-01"],  # Semana 1, Rodada 1
    ["2024-06-02"],  # Semana 1, Rodada 2
    ["2024-06-08"],  # Semana 2, Rodada 3
    ["2024-06-09"],  # Semana 2, Rodada 4
    ["2024-06-15"],  # Semana 3, Rodada 5
    ["2024-06-16"],  # Semana 3, Rodada 6
    ["2024-06-22"],  # Semana 4, Rodada 7
    ["2024-06-23"],  # Semana 4, Rodada 8
    ["2024-06-28"],  # Semana 5 (Super Semana), Rodada 9
    ["2024-06-29"],  # Semana 5 (Super Semana), Rodada 10
    ["2024-06-30"],  # Semana 5 (Super Semana), Rodada 11
    ["2024-07-12"],  # Semana 6 (Super Semana), Rodada 12
    ["2024-07-13"],  # Semana 6 (Super Semana), Rodada 13
    ["2024-07-14"],  # Semana 6 (Super Semana), Rodada 14
    ["2024-07-20"],  # Semana 7, Rodada 15
    ["2024-07-21"],  # Semana 7, Rodada 16
    ["2024-07-27"],  # Semana 8, Rodada 17
    ["2024-07-28"],  # Semana 8, Rodada 18
    ["2024-08-03","2024-08-04","2024-08-10","2024-08-11","2024-08-18"], # Upper Bracket
    ["2024-08-09","2024-08-17","2024-08-23","2024-08-24"], # Lower Bracket
    ["2024-09-07"]   # Grande Final
]

rounds_list = [
    "Rodada 1",
    "Rodada 2",
    "Rodada 3",
    "Rodada 4",
    "Rodada 5",
    "Rodada 6",
    "Rodada 7",
    "Rodada 8",
    "Rodada 9",
    "Rodada 10",
    "Rodada 11",
    "Rodada 12",
    "Rodada 13",
    "Rodada 14",
    "Rodada 15",
    "Rodada 16",
    "Rodada 17",
    "Rodada 18",
    "Chave Superior",
    "Chave Inferior",
    "Grande Final"
]

lol_df = df_gen.create_lol_dataframe(lol_csv_path)

cblol_df = df_gen.create_league_dataframe(lol_df, "CBLOL")

for i, date_filter in enumerate(date_filter_list):
    cblol_date_filtered_df = df_gen.filter_league_dataframe_by_date(cblol_df, date_filter)

    cblol_player_analysis_df = df_gen.create_player_analysis_dataframe(cblol_date_filtered_df, date_filter, rounds_list[i])

    cblol_top10_list = analysis.create_top10_dict_list(cblol_player_analysis_df)

    first_blood_score_insert = analysis.insert_first_blood_score(cblol_player_analysis_df)

    cblol_player_analysis_list = analysis.create_player_analysis_dict_list(cblol_player_analysis_df)

    conn.create_top10(cblol_top10_list)
    conn.create_info_player_record(cblol_player_analysis_list)

player_info_list = conn.get_info_player()
player_info_df = df_gen.create_dataframe_from_list(player_info_list)

all_top10_list = conn.get_top10()
all_top10_df = df_gen.create_dataframe_from_list(all_top10_list)

player_info_df.to_csv("extras/csv/player_info.csv", index=False)
all_top10_df.to_csv("extras/csv/top10.csv", index=False)

