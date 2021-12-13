import json
import ast
import os
import pandas as pd

from musedashboard.history_interface import ListeningHistory


class CSVHistory(ListeningHistory):
    def get_df_history():
        with open("config.json") as f:
            config = json.load(f)

        DIR_PATH = config["folder_path"]
        OUTPUT_NAME_FILE = [
            name for name in os.listdir(DIR_PATH) if name.endswith(".csv")
        ][0]
        OUTPUT_PATH_FILE = f"{DIR_PATH}/{OUTPUT_NAME_FILE}"
        DF_HISTORY = pd.read_csv(OUTPUT_PATH_FILE, index_col=0).drop(
            columns=["time_between_listening_seconds"]
        )

        genra_list = set()

        def add_to_set(genres):
            if type(genres) is str:
                for genre in ast.literal_eval(genres):
                    genra_list.add(genre)

        DF_HISTORY["genres"].apply(lambda genre: add_to_set(genre))
        genra_list = list(genra_list)

        for genre in genra_list:
            attrs = {
                genre: [
                    type(elem) is str and genre in elem for elem in DF_HISTORY["genres"]
                ]
            }
            DF_HISTORY = DF_HISTORY.assign(**attrs)

        return DF_HISTORY
