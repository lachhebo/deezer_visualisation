import os

import pandas as pd
from pymongo import MongoClient

from musedashboard.data_eng.api_manager import get_music_history
from musedashboard.data_eng.data_processing import process_track_history


class MongoJobFlow:
    @staticmethod
    def save_history_in_mongo_db():
        access_token, mongo_db_password, user_id = MongoJobFlow._get_env_variables()

        df_history_curated = MongoJobFlow.get_music_dataset(access_token, user_id)

        client = MongoClient(
            f"mongodb+srv://musedashboardstreamlit:{mongo_db_password}@cluster0.y9fcp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        )
        df_app_muse = MongoJobFlow.get_df_history_app(client)

        df_new_app_muse = pd.concat([df_history_curated, df_app_muse])
        df_without_duplicates = df_new_app_muse.drop_duplicates(
            subset=["timestamp"], ignore_index=True
        ).drop(columns=["_id"])

        client.muse_dashboard.history.drop()
        client.muse_dashboard.history.insert_many(
            df_without_duplicates.to_dict("records")
        )

    @staticmethod
    def get_df_history_app(client):
        collection = client.muse_dashboard.history
        df_in_database = pd.DataFrame(list(collection.find()))
        return df_in_database

    @staticmethod
    def get_music_dataset(access_token, user_id):
        music_history = get_music_history(access_token, user_id)
        df_history = pd.DataFrame(music_history)
        df_history_curated = process_track_history(df_history)
        return df_history_curated

    @staticmethod
    def _get_env_variables():
        from dotenv import load_dotenv

        load_dotenv()

        access_token = os.getenv("ACCESS_TOKEN")
        user_id = os.getenv("DEEZER_ID")
        mongo_db_password = os.getenv("MONGO_DB_PASSWORD")
        return access_token, mongo_db_password, user_id
