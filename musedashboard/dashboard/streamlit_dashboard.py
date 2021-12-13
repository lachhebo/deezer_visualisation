from musedashboard.dashboard.csv_history import CSVHistory
from musedashboard.dashboard.mongo_db_history import MongoHistory
import streamlit as st

st.set_page_config(
    page_title="MuseDashboard: a dashboard for deezer",
    page_icon="🎹",
)

st.write("Muse Dashboard: a dashboard that follow your music taste on deezer")


DF_HISTORY = MongoHistory.get_df_history()


st.write("Artists you listen the most")
st.write(DF_HISTORY.artist_name.value_counts()[0:20])

st.write("Albums you listen the most")
st.write(DF_HISTORY.album_name.value_counts()[0:20])

st.write("Title you listen the most")
st.write(DF_HISTORY.title.value_counts()[0:50])


st.write("Genres you listen the most")
fig, res = CSVHistory.get_plot_pie_df_history_genre_plot(DF_HISTORY)
st.pyplot(fig)
st.write(res)

# st.write("Genre evolution by date")
#
# fig1 = CSVHistory.get_genre_history_plot(DF_HISTORY)
# st.pyplot(fig1)
#
# fig3 = CSVHistory.get_music_listening_history_over_time_plot(DF_HISTORY)
#
# st.write("How much do you listen to music over time")
# st.pyplot(fig3)
