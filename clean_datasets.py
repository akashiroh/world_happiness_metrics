import pandas as pd
from pathlib import Path

def rename_gini(df: pd.DataFrame)->pd.DataFrame:
    """rename the columns of the gini df."""
    df = df.rename(columns={
        "gini__ppp_version_2021__poverty_line_no_poverty_line__welfare_type_income_or_consumption__table_income_or_consumption_consolidated__survey_comparability_no_spells": "gini_index",
        "Entity": "entity",
        "Code": "code",
        "Year": "year",
    })
    return df
def rename_whr(df: pd.DataFrame)->pd.DataFrame:
    """rename the columns of the whr df."""
    df = df.rename(columns={
        "Country name": "entity",
        "Ladder score": "ladder_score",
        "Standard error of ladder score": "ladder_score_std_err",
        "Logged GDP per capita": "log_gdp_per_capita",
        "Social support": "social_support",
        "Healthy life expectancy": "healthy_life_expectancy",
        "Freedom to make life choices": "freedom_to_make_life_choices",
        "Generosity": "generosity",
        "Perceptions of corruption": "perceptions_of_corruption",
        "Ladder score in Dystopia": "ladder_score_dystopia",
        "Explained by: Log GDP per capita": "explained_by_log_gdp_per_capita",
        "Explained by: Social support": "explained_by_social_support",
        "Explained by: Healthy life expectancy": "explained_by_healthy_life_expectancy",
        "Explained by: Freedom to make life choices": "explained_by_freedom_to_make_life_choices",
        "Explained by: Generosity": "explained_by_generosity",
        "Explained by: Perceptions of corruption": "explained_by_perceptions_of_corruption",
        "Dystopia + residual": "dystopia_residual",
    })
    return df


def clean_and_merge():
    """take the gini and whr datasets and merge them on country name for 2023."""

    DATA_DIR = Path("data")

    # load data
    gini_path = DATA_DIR / "gini_dataset.csv"
    whr_2023_path = DATA_DIR / "whr_2023_dataset.csv"
    gini_df = pd.read_csv(gini_path)
    whr_2023_df = pd.read_csv(whr_2023_path)

    collect = []
    for entity in gini_df["Entity"].unique():
        df = gini_df[gini_df["Entity"] == entity]

        if (2023 in df["Year"].tolist()) and (not df[df["Year"] == 2023]["gini__ppp_version_2021__poverty_line_no_poverty_line__welfare_type_income_or_consumption__table_income_or_consumption_consolidated__survey_comparability_no_spells"].isna().any()):
            collect.append(df)
        elif (2023 in df["Year"].tolist()) and (len(df) > 1):
            if df[df["Year"] == 2023]["gini__ppp_version_2021__poverty_line_no_poverty_line__welfare_type_income_or_consumption__table_income_or_consumption_consolidated__survey_comparability_no_spells"].isna().any():
                df["gini__ppp_version_2021__poverty_line_no_poverty_line__welfare_type_income_or_consumption__table_income_or_consumption_consolidated__survey_comparability_no_spells"] = df["gini__ppp_version_2021__poverty_line_no_poverty_line__welfare_type_income_or_consumption__table_income_or_consumption_consolidated__survey_comparability_no_spells"].fillna(df["gini__ppp_version_2021__poverty_line_no_poverty_line__welfare_type_income_or_consumption__table_income_or_consumption_consolidated__survey_comparability_no_spells"].mean())
                collect.append(df)
    gini_df = pd.concat(collect)

    # clean datasets
    gini_df = rename_gini(gini_df)
    whr_2023_df = rename_whr(whr_2023_df)
    gini_df = gini_df[gini_df["year"] == 2023]

    # select countries only in both datasets
    gini_countries = set(gini_df["entity"])
    whr_2023_countries = set(whr_2023_df["entity"])
    intersect = sorted(gini_countries.intersection(whr_2023_countries))

    gini_df = gini_df[gini_df["entity"].isin(intersect)]
    whr_2023_df = whr_2023_df[whr_2023_df["entity"].isin(intersect)]

    # left join
    merged = pd.merge(whr_2023_df, gini_df, on="entity", how="left")

    merged.to_csv(DATA_DIR / "merged.csv", index=False)
    print("Saved Merged Dataset to: ", DATA_DIR / "merged.csv")


if __name__ == "__main__":
    clean_and_merge()
