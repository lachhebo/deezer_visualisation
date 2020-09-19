import ast
from datetime import datetime

import pandas as pd

from api_manager import find_genres, find_bpm, find_release_date, find_gain, find_artist_fans, find_album_release_date,\
    find_album_fans


def drop_useless_column(df: pd.DataFrame):
    df = df.drop(columns=['type',
                          'readable',
                          'title_short',
                          'title_version',
                          'md5_image',
                          'preview',
                          'link',
                          'artist',
                          'album'])
    return df


def enrich_dataset_with_deezer_api_data(df: pd.DataFrame):
    df['genres'] = df['album'].apply(lambda x: find_genres(ast.literal_eval(x)))
    df['bpm'] = df['link'].apply(lambda x: find_bpm(x))
    df['gain'] = df['link'].apply(lambda x: find_gain(x))
    df['release_date'] = df['link'].apply(lambda x: find_release_date(x))
    df['artist_name'] = df['artist'].apply(lambda x: ast.literal_eval(x).get('name'))
    df['artist_fans'] = df['artist'].apply(lambda x: find_artist_fans(ast.literal_eval(x)))
    df['album_name'] = df['album'].apply(lambda x: ast.literal_eval(x).get('title'))
    df['album_release_date'] = df['album'].apply(lambda x: find_album_release_date(ast.literal_eval(x)))
    df['album_fans'] = df['album'].apply(lambda x: find_album_fans(ast.literal_eval(x)))
    return df


def process_track_history(path: str, write_path_folder: str):
    df_history = pd.read_csv(path).set_index('id')
    df_history = enrich_dataset_with_deezer_api_data(df_history)
    df_history['datetime'] = df_history['timestamp'].apply(lambda x: datetime.fromtimestamp(x))
    df_history = drop_useless_column(df_history)
    df_history = df_history.drop(columns=['timestamp'])
    df_history.to_csv(write_path_folder + path.split('/')[-1])


def process_favorite_tracks(path: str, write_path_folder: str):
    df_favorite = pd.read_csv(path).set_index('id')
    df_favorite = enrich_dataset_with_deezer_api_data(df_favorite)
    df_favorite['add_datetime'] = df_favorite['time_add'].apply(lambda x: datetime.fromtimestamp(x))
    df_favorite = drop_useless_column(df_favorite)
    df_favorite = df_favorite.drop(columns=['time_add'])
    df_favorite.to_csv(write_path_folder + path.split('/')[-1])
