import requests
import pandas as pd
import typer
from datetime import datetime

now = datetime.now()
app = typer.Typer()


def get_music_history(access_token, user_id):
    params_token = (
        ('access_token', access_token),
    )

    url = f'https://api.deezer.com/user/{user_id}/history&limit=1000'
    response = requests.get(url, params=params_token).json()
    result = response.get('data')

    url = response.get('next')
    response = requests.get(url, params=params_token).json().get('data')
    result = result + response
    return result


def get_music_favorite(access_token, user_id, limit=2000):
    params = (
        ('access_token', access_token),
    )

    url = f'https://api.deezer.com/user/{user_id}/playlists'
    playlist_list = requests.get(url, params=params).json().get('data')
    id_playlist = _find_loved_tracks_playlist(playlist_list)

    url_playlist = f'https://api.deezer.com/playlist/{id_playlist}&limit={limit}'
    response = requests.get(url_playlist, params=params).json().get('tracks').get('data')

    return response


def _find_loved_tracks_playlist(playlist_list):
    for playlist in playlist_list:
        if playlist['is_loved_track']:
            id_playlist = playlist['id']
    return id_playlist


@app.command()
def history(access_token: str, user_id: str, filename: str = 'listening_history'):
    history = get_music_history(access_token, user_id)
    history = pd.DataFrame(history).set_index('id')
    history.to_csv(filename + '_' + now.strftime('%Y-%m-%d') + '.csv')
    typer.echo(f'listening history saved in {filename}')


@app.command()
def favorite(access_token: str, user_id: str, filename: str = 'favorite_tracks'):
    favorite = get_music_favorite(access_token, user_id)
    favorite = pd.DataFrame(favorite).set_index('id')
    favorite.to_csv(filename + '_' + now.strftime('%Y-%m-%d') + '.csv')
    typer.echo(f'favorite tracks saved in {filename}')


if __name__ == '__main__':
    app()
