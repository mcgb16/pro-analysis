import pandas as pd

def create_lol_dataframe(csv_path):
    lol_df = pd.read_csv(csv_path , sep="," , dtype={'url': str})
    return lol_df