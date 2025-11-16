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

    df.to_csv(SAVE_DIR / "gini_dataset.csv", index=False)
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
