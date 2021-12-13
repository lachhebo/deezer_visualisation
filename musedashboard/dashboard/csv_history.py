import json
import ast
import os
import pandas as pd

from musedashboard.dashboard.history_interface import ListeningHistory


class CSVHistory(ListeningHistory):
    @staticmethod
    def get_df_history():
        with open("config.json") as f:
            config = json.load(f)

        dir_path = config["folder_path"]
        output_name_file = [
            name for name in os.listdir(dir_path) if name.endswith(".csv")
        ][0]
        output_path_file = f"{dir_path}/{output_name_file}"
        df_history = pd.read_csv(output_path_file, index_col=0).drop(
            columns=["time_between_listening_seconds"]
        )

        genra_list = set()

        def add_to_set(genres):
            if type(genres) is str:
                for genre in ast.literal_eval(genres):
                    genra_list.add(genre)

        df_history["genres"].apply(lambda genre: add_to_set(genre))
        genra_list = list(genra_list)

        for genre in genra_list:
            attrs = {
                genre: [
                    type(elem) is str and genre in elem for elem in df_history["genres"]
                ]
            }
            df_history = df_history.assign(**attrs)

        return df_history
