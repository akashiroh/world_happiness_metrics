# world_happiness_metrics
Group Final Project for Calling BS in AI

## Authors
- Andew Holmes
- Cooper Cox
- Aidan Chapman

## Installation Instructions
```
curl -LsSf https://astral.sh/uv/install.sh | sh

or

pip install uv
```

in the repo:
```
uv sync [optional flag] --no-cache
```

usage:
```
uv run main.py

or

source .venv/bin/activate
python3 main.py

uv add [python package]
```

## Dataset

- We use the [World Happieness Report 2023 Dataset](https://www.kaggle.com/datasets/ajaypalsinghlo/world-happiness-report-2023) and the [Gini Dataset](https://ourworldindata.org/grapher/economic-inequality-gini-index)
- Installation Instructions:
```
uv sync
uv run download_data.py # download gini and whr datasets
uv run clean_datasets.py # clean and merge them into one dataset
```

```
# download_data.py

import json
import requests
import pandas as pd
import kagglehub
import shutil
from pathlib import Path

def download_datasets():
    """download dataset to top-level data directory."""

    SAVE_DIR = Path(__file__).resolve().parent / "data"
    SAVE_DIR.mkdir(parents=True, exist_ok=True)

    # Gini Dataset
    df = pd.read_csv("https://ourworldindata.org/grapher/economic-inequality-gini-index.csv?v=1&csvType=full&useColumnShortNames=true", storage_options = {'User-Agent': 'Our World In Data data fetch/1.0'})
    metadata = requests.get("https://ourworldindata.org/grapher/economic-inequality-gini-index.metadata.json?v=1&csvType=full&useColumnShortNames=true").json()

    df.to_csv(SAVE_DIR / "gini_dataset.csv")
    print("Saved Gini Dataset to: ", SAVE_DIR / "gini_dataset.csv")
    with open(SAVE_DIR / "gini_metadata.csv", "w") as f: f.write(json.dumps(metadata))
    print("Saved Gini Metadata to: ", SAVE_DIR / "gini_metadata.json")


    # World Happiness Dataset
    download = Path(kagglehub.dataset_download("ajaypalsinghlo/world-happiness-report-2023"))
    dataset = list(download.glob("*.csv"))[0]
    shutil.move(str(dataset), SAVE_DIR / "whr_2023_dataset.csv")
    print("Saved WHR Dataset to: ", SAVE_DIR / "whr_2023_dataset.csv")

if __name__ == "__main__":
    download_datasets()
```

```
# clean_datasets.py

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
```
