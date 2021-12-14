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
        df_in_database2 = df_history.drop(columns=["_id"])
        df_in_database3 = df_in_database2[
            df_in_database2["genres"].apply(lambda x: type(x) == list)
        ]
        df_in_database3["primary_genre"] = df_in_database3["genres"].apply(
            lambda x: x[0] if len(x) > 0 else None
        )
        gender_proportion = df_in_database3.primary_genre.value_counts()
        fig, ax = plt.subplots(facecolor="black")  # solved by add this line

        ax = gender_proportion.plot.pie(  # noqa
            figsize=(50, 50), subplots=True, textprops={"color": "r"}
        )

        return fig, gender_proportion

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
