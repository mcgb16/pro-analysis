import db_conn as conn

def create_top10_dict_list(league_player_analysis_df):
    scores = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    columns_to_score = [
        "kda", "dpm", "vspm", "cspm", "wcpm", "wpm", "earned gpm", "geff", "geff team", "xpdiffat15", "csdiffat15", "golddiffat15", "kp"
    ]

    top10_list = []

    for column in columns_to_score:
        top10_df = league_player_analysis_df.nlargest(10, column)[["playername",column]]
        
        for rank, score in enumerate(scores):
            if rank < len(top10_df):
                playernames = top10_df.iloc[rank]["playername"]
                league_player_analysis_df.loc[
                    league_player_analysis_df["playername"] == playernames, 
                    "total_score"
                ] += score

                top10_dict = {
                    "sector": column,
                    "split" : league_player_analysis_df["split"].iloc[0],
                    "patch" : league_player_analysis_df["patch"].iloc[0],
                    "date" : league_player_analysis_df["date"].iloc[0],
                    "playoffs" : int(league_player_analysis_df["playoffs"].iloc[0]),
                    "rank": rank + 1,
                    "playername": playernames,
                    "value": top10_df.iloc[rank][column],
                    "score" : score
                }
                
                top10_list.append(top10_dict.copy())
    return top10_list

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