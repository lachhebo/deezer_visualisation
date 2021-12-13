import os
from datetime import datetime

import pandas as pd
import typer
import time

from musedashboard.data_eng.api_manager import get_music_history, get_music_favorite
from musedashboard.data_eng.data_processing import (
    process_track_history,
    process_favorite_tracks,
)
from musedashboard.mongo_job_flow import MongoJobFlow

now = datetime.now()
app = typer.Typer()


@app.command()
def process_history_folder(root_folder_path: str):
    input_dir_path = f"{root_folder_path}/listening_history"
    output_dir_path = f"{root_folder_path}/curated/listening_history"
    backup_dir_path = f"{root_folder_path}/backup/listening_history"
    files = os.listdir(input_dir_path)

    for file_name in files:
        try:
            if ".csv" in file_name:
                input_file_name = f"{input_dir_path}/{file_name}"
                history_df: pd.DataFrame = pd.read_csv(input_file_name).set_index("id")
                df_temp_worked: pd.DataFrame = process_track_history(
                    history_df
                ).set_index("timestamp")
                output_file_name = f"{output_dir_path}/{file_name.split('/')[-1]}"
                df_temp_worked.to_csv(output_file_name)
                os.rename(input_file_name, f"{backup_dir_path}/{file_name}")
        except Exception as e:
            print(e)


@app.command()
def process_curated_history_folder(root_folder_path: str):
    input_dir_path = f"{root_folder_path}/curated/listening_history"
    output_dir_path = f"{root_folder_path}/apps"
    backup_dir_path = f"{root_folder_path}/backup/apps"
    files = os.listdir(input_dir_path)
    file_output = os.listdir(output_dir_path)
    for filename in file_output:
        if ".csv" in filename:
            old_filename = filename
            df_all = pd.read_csv(f"{output_dir_path}/{filename}", index_col=0)

    for filename in files:
        if ".csv" in filename:
            input_file_name = f"{input_dir_path}/{filename}"
            df_new = pd.read_csv(input_file_name)
            df_all = pd.concat([df_all, df_new])
            os.rename(input_file_name, f"{backup_dir_path}/{filename}")

    df_all = df_all.drop_duplicates(subset=["timestamp"], ignore_index=True)
    df_all.to_csv(f"{output_dir_path}/output_result_{now.strftime('%Y-%m-%d-%H')}.csv")
    time.sleep(10)
    os.rename(f"{output_dir_path}/{old_filename}", f"{backup_dir_path}/{old_filename}")


@app.command()
def process_history(file_path: str, folder_to_save: str):
    df_history = pd.read_csv(file_path).set_index("id")
    df_history = process_track_history(df_history)
    df_history.to_csv(folder_to_save + file_path.split("/")[-1])


@app.command()
def process_favorites(file_path: str, folder_to_save: str):
    df_favorite = pd.read_csv(file_path).set_index("id")
    df_favorite = process_favorite_tracks(df_favorite)
    df_favorite.to_csv(folder_to_save + file_path.split("/")[-1])


@app.command()
def history(access_token: str, user_id: str, filename: str = "listening_history"):
    music_history = get_music_history(access_token, user_id)
    df_history = pd.DataFrame(music_history).set_index("id")
    df_history.to_csv(filename + "_" + now.strftime("%Y-%m-%d-%H") + ".csv")
    typer.echo(f"listening history saved in {filename}")


@app.command()
def favorite(access_token: str, user_id: str, filename: str = "favorite_tracks"):
    favorite_musics = get_music_favorite(access_token, user_id)
    df_favorite = pd.DataFrame(favorite_musics).set_index("id")
    df_favorite.to_csv(filename + "_" + now.strftime("%Y-%m-%d-%H") + ".csv")
    typer.echo(f"favorite tracks saved in {filename}")


@app.command()
def history2():
    MongoJobFlow.save_history_in_mongo_db()


if __name__ == "__main__":
    app()
