from datetime import datetime

import pandas as pd
import typer

from api_manager import get_music_history, get_music_favorite
from data_processing import process_track_history, process_favorite_tracks

now = datetime.now()
app = typer.Typer()


@app.command()
def process_history(file_path: str, folder_to_save: str):
    process_track_history(file_path, folder_to_save)


@app.command()
def process_favorites(file_path: str, folder_to_save: str):
    process_favorite_tracks(file_path, folder_to_save)


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
