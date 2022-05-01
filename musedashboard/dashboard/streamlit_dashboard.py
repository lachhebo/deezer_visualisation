from musedashboard.dashboard.mongo_db_history import MongoHistory
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="MuseDashboard: a dashboard for deezer",
    page_icon="🎹",
)

st.title("Muse Dashboard: follow your music taste")


DF_HISTORY = MongoHistory.get_df_history()


st.header("Top artists")
fig = px.bar(
    DF_HISTORY.artist_name.value_counts()[0:50], height=1000, orientation="h", width=800
)
st.plotly_chart(fig)

st.header("Top Albums")
fig = px.bar(
    DF_HISTORY.album_name.value_counts()[0:50], height=1000, orientation="h", width=800
)
st.plotly_chart(fig)
st.write(DF_HISTORY.album_name.value_counts()[0:100])

st.header("Top tracks")
fig = px.bar(
    DF_HISTORY.title.value_counts()[0:50], height=1000, orientation="h", width=800
)
st.plotly_chart(fig)
st.write(DF_HISTORY.title.value_counts()[0:100])


st.header("Top Genres")
fig = MongoHistory.get_plot_pie_df_history_genre_plot(DF_HISTORY)
st.plotly_chart(fig)


# st.write("Genre evolution by date")
#
# fig1 = CSVHistory.get_genre_history_plot(DF_HISTORY)
# st.pyplot(fig1)
#
# fig3 = CSVHistory.get_music_listening_history_over_time_plot(DF_HISTORY)
#
# st.write("How much do you listen to music over time")
# st.pyplot(fig3)
