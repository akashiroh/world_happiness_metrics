import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def plot_hists():
    """explore the dataset for trends."""

    DATA_DIR = Path("data")

    # load data
    data_path = DATA_DIR / "merged.csv"
    df = pd.read_csv(data_path)

    fig, axes = plt.subplots(1, 2, figsize=(12, 8))

    for i, col in enumerate(["ladder_score", "gini_index"]):
        axes[i].hist(df[col])
        axes[i].set_title(col)

    plt.savefig("test.png")

def explore():
    DATA_DIR = Path("data")

    # load data
    data_path = DATA_DIR / "countries_with_nans.csv"
    df = pd.read_csv(data_path)

    for entity in df["entity"].unique()[:20]:
        ent_df = df[df["entity"] == entity]
        plt.plot(ent_df["gini_index"])
    plt.savefig("nans.png")


if __name__ == "__main__":
    explore()
