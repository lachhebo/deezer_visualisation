import requests

DEEZER_API_URL = "https://api.deezer.com"


def _find_loved_tracks_playlist(playlist_list):
    for playlist in playlist_list:
        if playlist["is_loved_track"]:
            id_playlist = playlist["id"]
            return id_playlist
    raise (ValueError, "missing love tracks playlist")


def find_genres(album: dict):
    url = f'{DEEZER_API_URL}/album/{album.get("id")}'
    album_data = requests.get(url).json()
    if album_data.get("genres") is None:
        return album_data.get("genre_id")
    else:
        return [genre.get("name") for genre in album_data.get("genres").get("data")]


def find_album_release_date(album: dict):
    url = f'{DEEZER_API_URL}/album/{album.get("id")}'
    album_data = requests.get(url).json()
    return album_data.get("release_date")


def find_album_fans(album: dict):
    url = f'{DEEZER_API_URL}/album/{album.get("id")}'
    album_data = requests.get(url).json()
    return album_data.get("fans")


def find_artist_fans(artist: dict):
    url = f'{DEEZER_API_URL}/artist/{artist.get("id")}'
    album_data = requests.get(url).json()
    return album_data.get("nb_fan")


def find_bpm(track: str):
    url = f'{DEEZER_API_URL}/track/{track.split("/")[-1]}'
    album_data = requests.get(url).json()
    return album_data.get("bpm")


def find_gain(track: str):
    url = f'{DEEZER_API_URL}/track/{track.split("/")[-1]}'
    album_data = requests.get(url).json()
    return album_data.get("gain")


def find_release_date(track: str):
    url = f'{DEEZER_API_URL}/track/{track.split("/")[-1]}'
    album_data = requests.get(url).json()
    return album_data.get("release_date")


def get_music_history(access_token: str, user_id: str):
    params_token = (("access_token", access_token),)

    url = f"{DEEZER_API_URL}/user/{user_id}/history&limit=1000"
    response = requests.get(url, params=params_token).json()
    result = response.get("data")

    return result


def get_music_favorite(access_token: str, user_id: str, limit: int = 2000):
    params = (("access_token", access_token),)

    url = f"{DEEZER_API_URL}/user/{user_id}/playlists"
    playlist_list = requests.get(url, params=params).json().get("data")
    id_playlist = _find_loved_tracks_playlist(playlist_list)

    url_playlist = f"{DEEZER_API_URL}/playlist/{id_playlist}&limit={limit}"
    response = (
        requests.get(url_playlist, params=params).json().get("tracks").get("data")
    )

    return response
