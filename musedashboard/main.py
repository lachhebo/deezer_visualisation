import os
from datetime import datetime

import pandas as pd
import typer

from musedashboard.api_manager import get_music_history, get_music_favorite
from musedashboard.data_processing import process_track_history, process_favorite_tracks

now = datetime.now()
app = typer.Typer()


@app.command()
def process_history_folder(folder_path: str):
    files = os.listdir(folder_path)

    concatenate_df = pd.read_csv(f'{folder_path}/{files[0]}').set_index('timestamp')

    for file in files:
        df_temp = pd.read_csv(f'{folder_path}/{file}')
        df_temp_worked = process_track_history(df_temp).set_index('timestamp')
        concatenate_df = pd.concat([concatenate_df, df_temp_worked]).drop_duplicates()


@app.command()
def process_history(file_path: str, folder_to_save: str):
    df_history = pd.read_csv(file_path).set_index('id')
    df_history = process_track_history(df_history)
    df_history.to_csv(folder_to_save + file_path.split('/')[-1])


@app.command()
def process_favorites(file_path: str, folder_to_save: str):
    df_favorite = pd.read_csv(file_path).set_index('id')
    df_favorite = process_favorite_tracks(df_favorite)
    df_favorite.to_csv(folder_to_save + file_path.split('/')[-1])


@app.command()
def history(access_token: str, user_id: str, filename: str = 'listening_history'):
    music_history = get_music_history(access_token, user_id)
    df_history = pd.DataFrame(music_history).set_index('id')
    df_history.to_csv(filename + '_' + now.strftime('%Y-%m-%d-%H') + '.csv')
    typer.echo(f'listening history saved in {filename}')


@app.command()
def favorite(access_token: str, user_id: str, filename: str = 'favorite_tracks'):
    favorite_musics = get_music_favorite(access_token, user_id)
    df_favorite = pd.DataFrame(favorite_musics).set_index('id')
    df_favorite.to_csv(filename + '_' + now.strftime('%Y-%m-%d-%H') + '.csv')
    typer.echo(f'favorite tracks saved in {filename}')


if __name__ == '__main__':
    app()
