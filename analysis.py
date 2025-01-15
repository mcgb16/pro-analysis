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

def create_player_analysis_dict_list(league_player_analysis_df):
    player_analysis_list = league_player_analysis_df.to_dict(orient="records")

    return player_analysis_list