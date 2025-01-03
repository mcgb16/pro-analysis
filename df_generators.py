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
    league_filtered_df = league_df[league_df["date"].str.contains(date_filter)]

    return league_filtered_df