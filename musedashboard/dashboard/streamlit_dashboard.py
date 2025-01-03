from musedashboard.dashboard.mongo_db_history import MongoHistory
import streamlit as st
import plotly.express as px
import datetime as dt

st.set_page_config(
    page_title="MuseDashboard: a dashboard of your music tastes",
    page_icon="🎹",
)


@st.cache(ttl=60 * 60 * 1, allow_output_mutation=True)
def get_history():
    return MongoHistory.get_df_history()


DF_HISTORY = get_history()

def apply_filter(df_history):
    #return df_history
    return df_history[df_history.datetime > dt.datetime.now() - dt.timedelta(days=90)]

st.header("Top artists")
fig = px.bar(
    apply_filter(DF_HISTORY)
    .artist_name.str.replace(r"\(.*\)", "")
    .str.replace(r"\[.*\]", "")
    .str.strip()
    .str.lower()
    .value_counts()[0:50],
    height=1000,
    orientation="h",
    width=800,
)
st.plotly_chart(fig)
with st.expander("more"):
    st.dataframe(
        apply_filter(DF_HISTORY)
        .artist_name.str.replace(r"\(.*\)", "")
        .str.replace(r"\[.*\]", "")
        .str.strip()
        .str.lower()
        .value_counts()[50:]
    )

st.header("Top Albums")
fig = px.bar(
    apply_filter(DF_HISTORY)
    .album_name.str.replace(r"\(.*\)", "")
    .str.replace(r"\[.*\]", "")
    .str.strip()
    .str.lower()
    .str.replace("qalf infinity", "qalf")
    .str.replace("planet gold", "planet")
    .value_counts()[0:50],
    height=1000,
    orientation="h",
    width=800,
)
st.plotly_chart(fig)
with st.expander("more"):
    st.dataframe(
        apply_filter(DF_HISTORY)
        .album_name.str.replace(r"\(.*\)", "")
        .str.replace(r"\[.*\]", "")
        .str.strip()
        .str.lower()
        .str.replace("qalf infinity", "qalf")
        .str.replace("planet gold", "planet")
        .value_counts()[50:]
    )

st.header("Top tracks")
fig = px.bar(
    apply_filter(DF_HISTORY)
    # .title #str.replace(r"\(.*\)", "")
    # .str.replace(r"\[.*\]", "")
    .title.str.strip().value_counts()[0:50],
    height=1000,
    orientation="h",
    width=800,
)
st.plotly_chart(fig)
with st.expander("more"):
    st.write(
        apply_filter(DF_HISTORY)
        # .title.str.replace(r"\(.*\)", "")
        # .str.replace(r"\[.*\]", "")
        .title.str.strip().value_counts()[50:]
    )


st.header("Top Genres")
fig = MongoHistory.get_plot_pie_df_history_genre_plot(apply_filter(DF_HISTORY))
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
