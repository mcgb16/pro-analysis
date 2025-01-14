import db_conn as conn
import df_generators as df_gen
import plot_creation as plt
import analysis

lol_csv_path = "extras/2024_LoL_esports_match_data_from_OraclesElixir.csv"
date = input("Digite uma data (YYYY-MM-DD): ")
date_filter = []
date_filter.append(date)
split = "Split 1"
week = "Semana 1"
playoff = 0


lol_df = df_gen.create_lol_dataframe(lol_csv_path)

cblol_df = df_gen.create_league_dataframe(lol_df, "CBLOL")

cblol_date_filtered_df = df_gen.filter_league_dataframe_by_date(cblol_df, date_filter)

cblol_player_analysis_df = df_gen.create_player_analysis_dataframe(cblol_date_filtered_df)

cblol_top5_list = analysis.create_top5_dict_list(cblol_player_analysis_df)

first_blood_score_insert = analysis.insert_first_blood_score(cblol_player_analysis_df)

cblol_player_score_list = analysis.create_plscore_dict_list(cblol_player_analysis_df)

conn.create_top5(cblol_top5_list)

update_player = conn.update_player_record(cblol_player_score_list)

week_cblol_player_score_list = analysis.create_plweek_dict_list(cblol_player_analysis_df)
update_week_player = conn.update_week_player_record(week_cblol_player_score_list)

if not update_week_player:
    for i in week_cblol_player_score_list:
        i["date"] = [i["date"]]
    conn.create_week_player_record(week_cblol_player_score_list)

if not update_player:
    for i in cblol_player_score_list:
        i["date"] = [i["date"]]
    conn.create_player_record(cblol_player_score_list)

cblol_team_analysis_df = df_gen.create_team_dataframe(cblol_player_analysis_df)
cblol_team_score_list = analysis.create_team_dict_list(cblol_team_analysis_df)
week_cblol_team_score_list = analysis.create_team_week_dict_list(cblol_team_analysis_df)

update_team = conn.update_team_record(cblol_team_score_list)
update_week_team = conn.update_week_team_record(week_cblol_team_score_list)

if not update_week_team:
    for i in week_cblol_team_score_list:
        i["date"] = [i["date"]]
    conn.create_week_team_record(week_cblol_team_score_list)

if not update_team:
    for i in cblol_team_score_list:
        i["date"] = [i["date"]]
    conn.create_team_record(cblol_team_score_list)

pl_top5_list = analysis.create_pltop5_dict_list(split, playoff)

stage_player_list = conn.get_stage_player(split, playoff)
week_player_list = conn.get_week_player(split, week)
all_player_list = conn.get_player(split)

stage_player_df = df_gen.create_dataframe_from_list(stage_player_list)
week_player_df = df_gen.create_dataframe_from_list(week_player_list)
all_player_df = df_gen.create_dataframe_from_list(all_player_list)

# plt.create_sunburst_plot(cblol_top5_list)

# plt.create_icicle_plot(cblol_player_analysis_df, "Rodada")
# plt.create_icicle_plot(stage_player_df, "Fase")
# plt.create_icicle_plot(week_player_df, "Semana")
# plt.create_icicle_plot(all_player_df, "Camp Todo")