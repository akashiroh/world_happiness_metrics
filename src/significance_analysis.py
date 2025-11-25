import pandas as pd
from pathlib import Path
from scipy import stats
from exploration import plot_map
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# create map chart to determine the distribution of countries w/ low and high gini idex
def plot_gini_distribution(dataset: pd.DataFrame):
    fig = px.choropleth(
        dataset,
        locations="entity",
        locationmode="country names",
        color="gini_inequality",
        #color_continuous_scale=["blue", "red"]
        color_discrete_map={"high": "red", "low": "blue"}
    )

    plt.title("Distribution of high and low inequality countries")
    save_path = Path("figures/distribution_map.png")
    save_path.parent.mkdir(parents=True, exist_ok=True)
    fig.write_image(save_path)


# create function to get summary statistics and t-test results
def group_test(dataset: pd.DataFrame):
    high_inequality = dataset.groupby("gini_inequality").get_group("high")["ladder_score"]
    low_inequality = dataset.groupby("gini_inequality").get_group("low")["ladder_score"]

    norm_high_stat, norm_high_pval = stats.shapiro(high_inequality)
    norm_low_stat, norm_low_pval = stats.shapiro(low_inequality)
    print(f"Normality statistic high: {norm_high_stat}, Normality high p-value: {norm_high_pval}")
    print(f"Normality statistic low: {norm_low_stat}, Normality low p-value: {norm_low_pval}")

    levene_stat, levene_pval = stats.levene(high_inequality, low_inequality)
    print(f"Levene's statistic: {levene_stat}, Levene's p-value: {levene_pval}")

    t_stat, p_val = stats.ttest_ind(high_inequality, low_inequality)
    
    print(f"t-statistic: {t_stat}, p-value: {p_val}")
    ttest_boxplot(dataset)


# create plot (box and whiskers) to show results of t-test
def ttest_boxplot(dataset: pd.DataFrame):
    data = dataset[["ladder_score", "gini_inequality"]]
    boxplot = data.boxplot(by="gini_inequality")
    
    save_path = Path("figures/group_boxplot.png")
    save_path.parent.mkdir(parents=True, exist_ok=True)

    boxplot.set_ylabel("Ladder Score")
    boxplot.set_xlabel("Gini Inequality")
    plt.suptitle("Significance of high vs low inequality")
    plt.savefig(save_path)
    plt.close()


def top10_barplot(dataset: pd.DataFrame):
    top_data = dataset[["code", "ladder_score", "gini_index"]].sort_values(by="gini_index", ascending=False).head(10)
    bot_data = dataset[["code", "ladder_score", "gini_index"]].sort_values(by="gini_index").head(10)
    save_path = "figures/Top10"
    red_patch = mpatches.Patch(color="red", label="High inequality")
    blue_patch = mpatches.Patch(color="blue", label="Low inequality")

    ax = top_data.plot.bar(x="code", y="ladder_score", color="red", rot=0, fontsize=12)
    ax.legend(handles=[red_patch])
    plt.ylim(0, 8)

    ax.set_xlabel("Countries")
    ax.set_ylabel("Ladder Score")
    plt.suptitle("Top 10 most unequal countries and their average happiness")
    plt.tight_layout()
    plt.savefig(Path(save_path + "_unequal.png"))

    plt.close()

    ax = bot_data.plot.bar(x="code", y="ladder_score", color="blue", rot=0, fontsize=12)
    ax.legend(handles=[blue_patch])
    plt.ylim(0, 8)
    ax.set_xlabel("Countries")
    ax.set_ylabel("Ladder Score")

    plt.suptitle("Top 10 most equal countries and their average happiness")
    
    plt.tight_layout()
    plt.savefig(Path(save_path + "_equal.png"))
    plt.close()

    top10_happy = dataset.sort_values(by="ladder_score", ascending=False).head(10)
    colors = ["red" if x == "high" else "blue" for x in top10_happy["gini_inequality"]]

    ax = top10_happy.plot.bar(x="code", y="ladder_score", color=colors)
    ax.set_xlabel("Countries")
    ax.set_ylabel("Ladder Score") 
        
    ax.legend(handles=[red_patch, blue_patch])

    plt.ylim(0, 9)
   
    plt.suptitle("Top 10 happiest countries")
   
    plt.tight_layout()
    plt.savefig(Path(save_path + "_happiest.png"))
    plt.close()
 

def analyze_gini():
    data_dir = Path("data")
    merged_file = data_dir / "merged.csv"
    dataset = pd.read_csv(merged_file)

    gini_median = dataset["gini_index"].median()

    # separate into high and low groups
    dataset["gini_inequality"] = np.where(dataset["gini_index"] > gini_median, "high", "low")
    dataset["gini_inequality"] = dataset["gini_inequality"].astype("category")

    plot_gini_distribution(dataset)

    # conduct (independent?) two sample t-test
    group_test(dataset)

    top10_barplot(dataset)

if __name__ == "__main__":
    analyze_gini()
