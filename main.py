import db_conn as conn
import df_generators as df_gen
import analysis
import extras.info as ext

lol_csv_path = ext.csv_path

date_filter_list = ext.date_filter_list_split1

rounds_list = ext.rounds_list

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

