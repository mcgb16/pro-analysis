import db_conn as conn
import df_generators as df_gen
import analysis

lol_csv_path = "extras/2024_LoL_esports_match_data_from_OraclesElixir.csv"

date_filter_list = [
    "2024-01-20",  # Semana 1, Rodada 1
    "2024-01-21",  # Semana 1, Rodada 2
    "2024-01-27",  # Semana 2, Rodada 3
    "2024-01-28",  # Semana 2, Rodada 4
    "2024-02-03",  # Semana 3, Rodada 5
    "2024-02-04",  # Semana 3, Rodada 6
    "2024-02-10",  # Semana 4, Rodada 7
    "2024-02-11",  # Semana 4, Rodada 8
    "2024-02-17",  # Semana 5, Rodada 9
    "2024-02-18",  # Semana 5, Rodada 10
    "2024-02-24",  # Semana 6, Rodada 11
    "2024-02-25",  # Semana 6, Rodada 12
    "2024-03-02",  # Semana 7, Rodada 13
    "2024-03-03",  # Semana 7, Rodada 14
    "2024-03-09",  # Semana 8, Rodada 15
    "2024-03-10",  # Semana 8, Rodada 16
    "2024-03-16",  # Semana 9, Rodada 17
    "2024-03-17",  # Semana 9, Rodada 18
    ["2024-03-22",  # Fase Eliminatória, Rodada 1 Chave Superior [Série 1]
    "2024-03-23"],  # Fase Eliminatória, Rodada 1 Chave Superior [Série 2]
    ["2024-03-30",  # Fase Eliminatória, Semifinal Chave Superior [Série 3]
    "2024-03-31"],  # Fase Eliminatória, Semifinal Chave Superior [Série 4]
    ["2024-04-05",  # Fase Eliminatória, Rodada 1 Chave Inferior [Série 5]
    "2024-04-06"],  # Fase Eliminatória, Rodada 1 Chave Inferior [Série 6]
    "2024-04-07",  # Fase Eliminatória, Final da Chave Superior [Série 7]
    "2024-04-13",  # Fase Eliminatória, Rodada 2 Chave Inferior [Série 8]
    "2024-04-14",  # Fase Eliminatória, Final da Chave Inferior [Série 9]
    "2024-04-20"   # Fase Eliminatória, Grande Final [Série 10]
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
    "Rodada 1 Chave Superior",
    "Semifinal Chave Superior",
    "Rodada 1 Chave Inferior",
    "Final da Chave Superior",
    "Rodada 2 Chave Inferior",
    "Final da Chave Inferior",
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

