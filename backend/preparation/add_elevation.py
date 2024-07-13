import pandas as pd
import numpy as np
import requests
import argparse
import time

API_KEY = "ak_4xd9pBKL_M5J49F0WOU7ZIxdV"
BASE_URL = "https://api.gpxz.io/v1/elevation/points"

def add_elevation_column(df: pd.DataFrame,  header: bool = False):
    """
    Add elevation column to the dataframe. Save the updated dataframe to a csv file.

    Args:
        df (pd.DataFrame): The dataframe to add the altitude column to
        header (bool): Whether to write the header to the csv file. Default is False

    Returns:
        None
    """

    #Extract the latitude and longitude columns
    latlons: str = "|".join([f"{lat},{lon}" for lat, lon in zip(df['lat'], df['lon'])])

    url = f"{BASE_URL}?latlons={latlons}&api-key={API_KEY}&interpolation=nearest"
    print(url)
    response = requests.get(url)
    
    if response.status_code == 200:
        try:
            results = response.json()["results"]
            elevations = [result["elevation"] for result in results]
            df["elevation"] = df.apply(lambda x: elevations.pop(0), axis=1)
            df.to_csv("1950-2021_fires_with_elevation_2.csv", mode='a', header=header, index=False)
            print("Elevations added successfully.")
        except KeyError:
            print("Failed to get elevations. Response:", response);
    else:
        print("Failed to get elevations. Status code:", response.status_code)

def add_elevation(dfs: list[pd.DataFrame], start_index: int = 0, batch_limit: int = 1, wait_minutes: int = 10):
    """
    Add elevation to provided dataframes.

    Args:
        dfs (list[pd.DataFrame]): The list of dataframes to add elevation to
        start_index (int): The index to start from
        batch_limit (int): The number of batches to do before waiting
        wait_minutes (int): The number of minutes to wait after every batch_limit batches

    Returns:
        None
    """
    if start_index == 0:
        print("Adding altitude to the dataset...")
        print("Adding altitude to batch 1...")
        add_elevation_column(dfs[0], header=True)
        print("Batch 1 complete")
        start_index += 1

    for df in dfs[start_index:]:
        
        print(f"Adding altitude to batch {start_index}...")
        add_elevation_column(df)
        print(f"Batch {start_index} complete\n")
        start_index += 1
        time.sleep(wait_minutes * 60)

        if start_index % batch_limit == 0:
            print(f"{batch_limit} batches complete.")
            print(f"Waiting for {wait_minutes} minutes in order to avoid rate limiting...")

# Load the data
dataset = pd.read_csv("1950-2021_fires.csv")
#Split the df into batches of 50 data points
batch_size = 50
dfs = np.array_split(dataset, len(dataset) // batch_size)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add elevation to the dataset using the Canada elevation API.")
    parser.add_argument("--start-index", type=int, default=0,
                        help="The index to start from. Defaults to 0.")
    parser.add_argument("--batch-limit", type=int, default=1,
                        help="The number of batches to do before waiting. Defaults to 10.")
    parser.add_argument("--wait-minutes", type=int, default=10,
                        help="The number of minutes to wait after every batch_limit batches. Defaults to 10.")
    
    args = parser.parse_args()
    # add_elevation(dfs, args.start_index, args.batch_limit, args.wait_minutes)

    response = requests.get(
        url,
        headers={
            "x-api-key": API_KEY,
            "Content-Type": "application/json"
        },
        data="latlons=45.4215,-75.6972|45.4215,-75.6972&interpolation=nearest"
    )
    print(response.json())