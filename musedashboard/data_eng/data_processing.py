from datetime import datetime

import numpy as np
import pandas as pd

from musedashboard.data_eng.api_manager import (
    find_genres,
    find_bpm,
    find_release_date,
    find_gain,
    find_artist_fans,
    find_album_release_date,
    find_album_fans,
)

MINUTES_AFTER_MUSIC_DURATION_CONSIDERED = 5


def drop_useless_column(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(
        columns=[
            "type",
            "readable",
            "title_short",
            "title_version",
            "md5_image",
            "preview",
            "link",
            "artist",
            "album",
        ]
    )
    return df


def enrich_dataset_with_deezer_api_data(df: pd.DataFrame) -> pd.DataFrame:
    df["genres"] = df["album"].apply(lambda x: find_genres(x))
    df["bpm"] = df["link"].apply(lambda x: find_bpm(x))
    df["gain"] = df["link"].apply(lambda x: find_gain(x))
    df["release_date"] = df["link"].apply(lambda x: find_release_date(x))
    df["artist_name"] = df["artist"].apply(lambda x: x.get("name"))
    df["artist_fans"] = df["artist"].apply(lambda x: find_artist_fans(x))
    df["album_name"] = df["album"].apply(lambda x: x.get("title"))
    df["album_release_date"] = df["album"].apply(lambda x: find_album_release_date(x))
    df["album_fans"] = df["album"].apply(lambda x: find_album_fans(x))
    return df


def get_times_listening_in_seconds(
    df_row, time_column: str, duration_column: str
) -> float:
    max_listening_time = abs(df_row[time_column])
    duration = df_row[duration_column]
    if max_listening_time > duration:
        time_between_listening = max_listening_time - duration
        if time_between_listening < MINUTES_AFTER_MUSIC_DURATION_CONSIDERED * 60:
            return duration
        else:
            return np.nan
    else:
        return max_listening_time


def compute_listening_time(df: pd.DataFrame, data_column: str) -> pd.DataFrame:
    df = df.sort_values(by=data_column)
    df["time_between_listening"] = df[data_column].diff(periods=-1)
    df["time_between_listening_seconds"] = df["time_between_listening"].apply(
        lambda x: x.total_seconds()
    )
    df["listening_time"] = df.apply(
        lambda x: get_times_listening_in_seconds(
            x, "time_between_listening_seconds", "duration"
        ),
        axis=1,
    )
    df = df.drop(columns=["time_between_listening"])
    return df


def process_track_history(df: pd.DataFrame) -> pd.DataFrame:
    df_history = enrich_dataset_with_deezer_api_data(df)
    df_history["datetime"] = df_history["timestamp"].apply(
        lambda x: datetime.fromtimestamp(x)
    )
    df_history = compute_listening_time(df_history, "datetime")
    df_history = drop_useless_column(df_history)
    return df_history


def process_favorite_tracks(df: pd.DataFrame) -> pd.DataFrame:
    df_favorite = enrich_dataset_with_deezer_api_data(df)
    df_favorite["add_datetime"] = df_favorite["time_add"].apply(
        lambda x: datetime.fromtimestamp(x)
    )
    df_favorite = drop_useless_column(df_favorite)
    df_favorite = df_favorite.drop(columns=["time_add"])
    return df_favorite
