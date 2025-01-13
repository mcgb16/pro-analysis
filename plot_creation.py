import plotly.express as px
import pandas as pd

def create_sunburst_plot(top5_list):
    data = {
        "sector": [],
        "player": [],
        "value": [],
        "score": []
    }

    for entry in top5_list:
        sector = entry["sector"]
        for playername, stats in entry.items():
            if playername not in ["sector", "split", "patch", "date", "playoffs"]:
                data["sector"].append(sector)
                data["player"].append(playername)
                data["value"].append(stats["value"])
                data["score"].append(stats["score"])

    df = pd.DataFrame(data)

    fig = px.sunburst(
        df,
        path=["sector", "player","value"],
        values="score",
        title="Sunburst Plot dos Top 5 Jogadores",
    )

    fig.update_traces(hovertemplate="")

    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))

    fig.show()

    return

def create_icicle_plot(league_player_analysis_df, custom_title):
    top_5_players = league_player_analysis_df.nlargest(5, "total_score")
    top_3_per_lane = league_player_analysis_df.groupby("position").apply(lambda x: x.nlargest(3, "total_score")).reset_index(drop=True)
    top_1_per_lane = league_player_analysis_df.groupby("position").apply(lambda x: x.nlargest(1, "total_score")).reset_index(drop=True)

    hierarchical_data = []
    
    # Top 5
    for _, player in top_5_players.iterrows():
        player_data = {
            "level_1": "Top 5 Players",
            "level_2": player["playername"],
            "score": player["total_score"]
        }
        hierarchical_data.append(player_data)
    
    # Top 3 por lane
    for _, player in top_3_per_lane.iterrows():
        player_data = {
            "level_1": "Top 3 per Lane",
            "level_2": player["position"],
            "level_3": player["playername"],
            "score": player["total_score"]
        }
        hierarchical_data.append(player_data)
    
    # Top 1 por lane
    for _, player in top_1_per_lane.iterrows():
        player_data = {
            "level_1": "Top 1 per Lane",
            "level_2": player["position"],
            "level_3": player["playername"],
            "score": player["total_score"]
        }
        hierarchical_data.append(player_data)
    
    df = pd.DataFrame(hierarchical_data)
    
    fig = px.icicle(
        df,
        path=["level_1", "level_2", "level_3"],
        values="score",
        title=custom_title,
    )
    
    fig.update_traces(hovertemplate="")

    fig.show()

    return