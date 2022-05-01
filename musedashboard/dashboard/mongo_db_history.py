from pymongo import MongoClient
import pandas as pd
import os
import ast

from musedashboard.dashboard.history_interface import ListeningHistory


class MongoHistory(ListeningHistory):
    @staticmethod
    def get_df_history():
        from dotenv import load_dotenv

        load_dotenv()
        mongo_db_password = os.getenv("MONGO_DB_PASSWORD", "")
        client = MongoClient(
            f"mongodb+srv://musedashboardstreamlit:{mongo_db_password}@cluster0.y9fcp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        )
        collection = client.muse_dashboard.history
        df_history = pd.DataFrame(list(collection.find()))

        df_in_database2 = df_history.drop(columns=["_id"])

        def try_or(x):
            try:
                return ast.literal_eval(x)
            except Exception:
                return []

        df_in_database2["genres_f"] = df_in_database2["genres"].apply(
            lambda x: x if type(x) == list else try_or(x)
        )

        df_in_database2["primary_genre"] = df_in_database2["genres_f"].apply(
            lambda x: x[0] if len(x) > 0 else None
        )

        return df_in_database2
