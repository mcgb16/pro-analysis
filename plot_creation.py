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