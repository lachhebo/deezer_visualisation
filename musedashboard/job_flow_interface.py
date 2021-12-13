import pandas as pd
import abc


class JobDeezerFlow:
    @abc.abstractstaticmethod
    def write_favorite(df: pd.DataFrame):
        pass

    @abc.abstractstaticmethod
    def get_history():
        pass

    @abc.abstractstaticmethod
    def write_history(df: pd.DataFrame):
        pass

    @abc.abstractstaticmethod
    def write_curated_history(df: pd.DataFrame):
        pass

    @abc.abstractstaticmethod
    def get_curated_history():
        pass

    @abc.abstractstaticmethod
    def write_app_history(df: pd.DataFrame):
        pass
