import db_conn as conn

def create_top10_dict_list(league_player_analysis_df):
    scores = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    columns_to_score = [
        "kda", "dpm", "vspm", "cspm", "wcpm", "wpm", "earned gpm", "geff", "geff team", "xpdiffat15", "csdiffat15", "golddiffat15", "kp"
    ]

    top10_list = []

    for column in columns_to_score:
        # Sort the DataFrame by the current column in descending order
        sorted_df = league_player_analysis_df.sort_values(by=column, ascending=False)

        for rank, (index, row) in enumerate(sorted_df.iterrows()):
            score = scores[rank] if rank < len(scores) else 0  # Assign score based on rank

            top10_dict = {
                "sector": column,
                "split": row["split"], # Access values directly from the row
                "patch": row["patch"],
                "round": row["round"],
                "playoffs": int(row["playoffs"]),
                "rank": rank + 1,
                "playername": row["playername"],
                "value": row[column],
                "score": score
            }

            top10_list.append(top10_dict.copy())
            
            # Update the total score in the original DataFrame (only for top 10)
            if score > 0:
                league_player_analysis_df.loc[index, "total_score"] += score


    return top10_list

def insert_first_blood_score(league_player_analysis_df):
    league_player_analysis_df["total_score"] += (
        league_player_analysis_df["firstbloodkill"] * 3
        + league_player_analysis_df["firstbloodassist"] * 3
        - league_player_analysis_df["firstbloodvictim"] * 3
    )
    
    return

def create_player_analysis_dict_list(league_player_analysis_df):
    player_analysis_list = league_player_analysis_df.to_dict(orient="records")

    return player_analysis_list