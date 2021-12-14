import pandas as pd
import abc
import matplotlib.pyplot as plt
import dateutil


class ListeningHistory:
    @staticmethod
    @abc.abstractmethod
    def get_df_history():
        pass

    @staticmethod
    def get_plot_pie_df_history_genre_plot(df_history: pd.DataFrame):
        genres_sr = df_history[
            [
                "Trance",
                "Rap/Hip Hop",
                "R&B contemporain",
                "R&B",
                "Electro",
                "Jeunesse",
                "Latino",
                "Soul contemporaine",
                "Alternative",
                "Films/Jeux vidéo",
                "Bandes originales",
                "Jazz",
                "Comédies musicales",
                "Moderne",
                "Techno/House",
                "Musique africaine",
                "Musiques de films",
                "Classique",
                "Dance",
                "Musiques de jeux vidéo",
                "Pop indé/Folk",
                "Chill Out/Trip-Hop/Lounge",
                "Reggae",
                "Musique asiatique",
                "Musique arabe",
                "Soul & Funk",
                "Soul",
                "Singer & Songwriter",
                "Chanson française",
                "Folk",
                "Pop",
                "Pop Indé",
                "Pop internationale",
                "Metal",
                "Hard Rock",
                "Electro Pop/Electro Rock",
                "Rock",
                "Rock indé",
                "Rock Indé/Pop Rock",
                "Variété Internationale",
            ]
        ].sum()

        aller = pd.Series([genres_sr[genres_sr < 150].sum()], index=["others"])
        fig, ax = plt.subplots(facecolor="black")  # solved by add this line

        genres_sr = genres_sr.append(aller)
        ax = genres_sr[genres_sr >= 150].plot.pie(  # noqa
            figsize=(50, 50), subplots=True, textprops={"color": "w"}
        )

        return fig, genres_sr

    @staticmethod
    def get_genre_history_plot(df_history):
        ts = df_history[
            [
                "datetime",
                "Rap/Hip Hop",
                "Rock",
                "Pop",
                "Metal",
                "Alternative",
                "Electro",
                "Musiques de films",
            ]
        ].sort_values("datetime")
        ts["datetime"] = ts["datetime"].apply(dateutil.parser.parse)
        ts = ts.set_index("datetime")

        fig, ax = plt.subplots()  # solved by add this line
        data_resample = ts.resample("1W").sum()

        data_resample.plot(figsize=(20, 10), ax=ax, title="genre listening over time")

        return fig

    @staticmethod
    def get_music_listening_history_over_time_plot(df_history):
        ts = df_history[["datetime", "duration"]].sort_values("datetime")
        ts["datetime"] = ts["datetime"].apply(dateutil.parser.parse)
        ts = ts.set_index("datetime")
        fig, ax = plt.subplots()  # solved by add this line

        data_resample = ts.resample("1W").count()
        data_resample.plot(figsize=(20, 13), title="music listening over time", ax=ax)

        return fig
