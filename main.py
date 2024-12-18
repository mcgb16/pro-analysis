import pandas as pd

lol_csv_path = "extras/2024_LoL_esports_match_data_from_OraclesElixir.csv"

lol_df = pd.read_csv(lol_csv_path , sep="," , dtype={'url': str})

cblol_df = lol_df[lol_df["league"] == "CBLOL"]