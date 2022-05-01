import pandas as pd
import abc
import plotly.express as px


class ListeningHistory:
    @staticmethod
    @abc.abstractmethod
    def get_df_history():
        pass

    @staticmethod
    def get_plot_pie_df_history_genre_plot(df_history: pd.DataFrame):
        gender_proportion = df_history.primary_genre.value_counts()
        fig = px.pie(
            gender_proportion,
            values="primary_genre",
            names=gender_proportion.index,
            height=1000,
        )

        return fig
