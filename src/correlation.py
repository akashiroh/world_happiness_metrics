import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from scipy.stats import pearsonr, spearmanr

def correlation():
    """compute the correlation between two variables."""

    DATA_DIR = Path("data")

    # load data
    data_path = DATA_DIR / "merged.csv"
    df = pd.read_csv(data_path)

    var1 = "gini_index"
    var2 = "ladder_score"

    plt.scatter(
        df[var1],
        df[var2],
    )
    plt.xlabel(var1)
    plt.ylabel(var2)
    plt.savefig("one-to-one.png")
    print("Saved figure: one-to-one.png")


    correlation, p_value = pearsonr(df[var1], df[var2])
    print(f"Pearson correlation: {correlation:.2f}")
    print(f"P-value: {p_value:.2f}")

    correlation, p_value = spearmanr(df[var1], df[var2])
    print(f"spearman correlation: {correlation:.2f}")
    print(f"P-value: {p_value:.2f}")


if __name__ == "__main__":
    correlation()
