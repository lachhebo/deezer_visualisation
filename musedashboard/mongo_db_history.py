from pymongo import MongoClient
import pandas as pd
import os

from musedashboard.history_interface import ListeningHistory


class MongoHistory(ListeningHistory):


    def get_df_history(df_history: pd.DataFrame):
        from dotenv import load_dotenv
        load_dotenv()
        mongo_db_password = os.getenv("MONGO_DB_PASSWORD", "")
        client = MongoClient(f"mongodb+srv://musedashboardstreamlit:{mongo_db_password}@cluster0.y9fcp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        collection = client.muse_dashboard.history
        df_history = pd.DataFrame(list(collection.find()))
        return df_history


