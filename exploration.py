import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from pathlib import Path

def plot_hists():
    """explore the dataset for trends."""

    DATA_DIR = Path("data")

    # load data
    data_path = DATA_DIR / "merged.csv"
    df = pd.read_csv(data_path)

    metric = "social_support"

    gini_2023 = df[df['year'] == 2023][['code', metric]]
    fig = px.choropleth(
        gini_2023,
        locations='code',
        color=metric,
        hover_name='code',
        color_continuous_scale='RdYlBu_r',
        title=f'{" ".join(map(str.capitalize, metric.split("_")))} 2023'
    )
    fig.show()


def explore():
    DATA_DIR = Path("data")

    # load data
    data_path = DATA_DIR / "countries_with_nans.csv"
    df = pd.read_csv(data_path)

    for entity in df["entity"].unique():
        ent_df = df[df["entity"] == entity]
        plt.plot(ent_df["year"], ent_df["gini_index"])
    plt.savefig("nans.png")


if __name__ == "__main__":
    plot_hists()
