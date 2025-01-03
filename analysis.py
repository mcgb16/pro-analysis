import db_conn as conn

def create_top5_dict_list(league_player_analysis_df):
    scores = [10, 8, 6, 4, 2]
    columns_to_score = [
        "kda", "dpm", "vspm", "cspm", "wcpm", "wpm", "earned gpm", "geff", "geff team", "xpdiffat15", "csdiffat15", "golddiffat15", "kp"
    ]

    top5_list = []

    for column in columns_to_score:
        top5_df = league_player_analysis_df.nlargest(5, column)[["playername",column]]

        top5_dict = {
            "sector": column,
            "split" : league_player_analysis_df["split"].iloc[0],
            "patch" : league_player_analysis_df["patch"].iloc[0],
            "date" : league_player_analysis_df["date"].iloc[0],
            "playoffs" : int(league_player_analysis_df["playoffs"].iloc[0])
        }
        
        for rank, score in enumerate(scores):
            if rank < len(top5_df):
                playernames = top5_df.iloc[rank]["playername"]
                league_player_analysis_df.loc[
                    league_player_analysis_df["playername"] == playernames, 
                    "total_score"
                ] += score

                top5_dict[playernames] = {
                    "value" : top5_df.iloc[rank][column],
                    "score" : score
                }
                
        top5_list.append(top5_dict.copy())
    return top5_list

def insert_first_blood_score(league_player_analysis_df):
    league_player_analysis_df["total_score"] += (
        league_player_analysis_df["firstbloodkill"] * 5
        + league_player_analysis_df["firstbloodassist"] * 5
        - league_player_analysis_df["firstbloodvictim"] * 5
    )
    
    return

def create_plscore_dict_list(league_player_analysis_df):
    score_filter = ["playername", "split", "playoffs", "date", "total_score"]

    league_player_score_list = league_player_analysis_df[score_filter].to_dict(orient="records")

    return league_player_score_list

def create_pltop5_dict_list(split, is_playoffs):
    player_search = conn.get_player(split, is_playoffs)

    pl_top5_list = []

    for i in player_search:
        top5_search = conn.get_top5(split, is_playoffs)
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

    return pl_top5_list