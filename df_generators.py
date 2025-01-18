import pandas as pd
import numpy as np

def create_lol_dataframe(csv_path):
    lol_df = pd.read_csv(csv_path , sep="," , dtype={'url': str})
    return lol_df

def create_league_dataframe(lol_df, league):
    lol_league_df = lol_df[lol_df["league"] == league].copy()
    lol_league_df['geff'] = lol_league_df['dpm'] / lol_league_df['earned gpm']
    lol_league_df['geff team'] = lol_league_df['damageshare'] / lol_league_df['earnedgoldshare']
    lol_league_df['kp'] = np.where(
        lol_league_df['teamkills'] > 5, 
        (lol_league_df["kills"] + lol_league_df["assists"]) / lol_league_df["teamkills"], 
        0
    )
    lol_league_df['kda'] = (lol_league_df["kills"] + lol_league_df["assists"]) / lol_league_df["deaths"].replace(0, np.nan)
    lol_league_df['kda'] = lol_league_df['kda'].fillna(lol_league_df["kills"] + lol_league_df["assists"])
    lol_league_df["csdiffat15"] = np.where(
        lol_league_df["position"] != "sup",
        lol_league_df["csdiffat15"],
        0
    )

    return lol_league_df

def filter_league_dataframe_by_date(league_df, date_filter):
    regex_date_filter = "|".join(date_filter)
    league_filtered_df = league_df[league_df["date"].str.contains(regex_date_filter)]

    return league_filtered_df

def create_player_analysis_dataframe(league_date_filtered_df):
    columns_player_analysis = [
    "playername",
    "teamname",
    "position",
    "kda",
    "dpm",
    "earned gpm",
    "geff",
    "wcpm",
    "wpm",
    "vspm",
    "cspm",
    "golddiffat15",
    "csdiffat15",
    "xpdiffat15",
    "firstbloodkill",
    "firstbloodassist",
    "firstbloodvictim",
    "damageshare",
    "earnedgoldshare",
    "geff team",
    "kp"
    ]

    player_analysis_agg_dict = {
        "position": "first",
        "teamname": "first",
        "kda": "mean",
        "dpm": "mean",
        "earned gpm": "mean",
        "geff": "mean",
        "wcpm": "mean",
        "wpm": "mean",
        "vspm": "mean",
        "cspm": "mean",
        "golddiffat15": "mean",
        "csdiffat15": "mean",
        "xpdiffat15": "mean",
        "firstbloodkill": "sum",
        "firstbloodassist": "sum",
        "firstbloodvictim": "sum",
        "damageshare": "mean",
        "earnedgoldshare": "mean",
        "geff team": "mean",
        "kp" : "mean"
    }

    round = input(f"Qual rodada essa data faz parte: ")
    
    needed_columns = {
        "total_score" : 0,
        "split" : league_date_filtered_df["split"].iloc[0],
        "patch" : float(league_date_filtered_df["patch"].iloc[0]),
        "date" : league_date_filtered_df["date"].iloc[0],
        "playoffs" : int(league_date_filtered_df["playoffs"].iloc[0]),
        "round" : round
    }

    league_player_analysis_df = league_date_filtered_df[columns_player_analysis].copy().groupby('playername').agg(player_analysis_agg_dict).reset_index()

    league_player_analysis_df = league_player_analysis_df.assign(**needed_columns)

    return league_player_analysis_df

def create_dataframe_from_list(dict_list):
    df = pd.DataFrame(dict_list)

    return df