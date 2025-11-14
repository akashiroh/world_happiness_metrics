import pandas as pd
from pathlib import Path


def clean_and_merge():
    """take the gini and whr datasets and merge them on country name for 2023."""

    DATA_DIR = Path("data")

    # load data
    gini_path = DATA_DIR / "gini_dataset.csv"
    whr_2023_path = DATA_DIR / "whr_2023_dataset.csv"
    gini_df = pd.read_csv(gini_path)
    whr_2023_df = pd.read_csv(whr_2023_path)

    # clean datasets
    gini_df = gini_df[gini_df["Year"] == 2023]
    whr_2023_df = whr_2023_df.rename(columns={"Country name": "Entity"})

    # select countries only in both datasets
    gini_countries = set(gini_df["Entity"])
    whr_2023_countries = set(whr_2023_df["Entity"])
    intersect = sorted(gini_countries.intersection(whr_2023_countries))

    gini_df = gini_df[gini_df["Entity"].isin(intersect)]
    whr_2023_df = whr_2023_df[whr_2023_df["Entity"].isin(intersect)]

    # left join
    merged = pd.merge(whr_2023_df, gini_df, on="Entity", how="left")

    merged.to_csv(DATA_DIR / "merged.csv", index=False)
    print("Saved Merged Dataset to: ", DATA_DIR / "merged.csv")


if __name__ == "__main__":
    clean_and_merge()
