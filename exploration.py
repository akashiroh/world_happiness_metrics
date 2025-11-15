import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from pathlib import Path

def plot_hists():
    """plot histograms."""

    DATA_DIR = Path("data")

    # load data
    data_path = DATA_DIR / "merged.csv"
    df = pd.read_csv(data_path)

    metric = "ladder_score"

    plt.figure(figsize=(12,6))

    plt.hist(
        df[metric]
    )
    plt.title(f'{" ".join(map(str.capitalize, metric.split("_")))} 2023')
    plt.xlabel(metric)
    plt.ylabel("count")
    plt.savefig(f"{metric}_hist.png")
    print("Saved figure:", f"{metric}_hist.png")



def plot_map():
    """plot map."""

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
