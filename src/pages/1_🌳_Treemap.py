import streamlit as st
import polars as pl

import hypothesis_row as hr
import treemap as tm


DATA_DIR = "data/"
MIN_ROW = 0
MAX_ROW = 21
DATA_FILES = {
    "BookCrossing": "book_crossing.csv",
    "Yelp": "yelp.csv",
    "MovieLens": "movie_lens.csv",
}
ALGORITHMS = {
    "Greedy": "Greedy-HEP",
    "Reinforcement Learning": "RL-HEP",
}
FONT_SIZE = 20


def main():
    dataset_options = [k for k in DATA_FILES]
    algo_options = [k for k in ALGORITHMS]

    dataset = st.sidebar.selectbox("Dataset", dataset_options)
    algorithm = ALGORITHMS[st.sidebar.selectbox("Algorithm", algo_options)]
    depth = st.sidebar.selectbox(
        "Depth", ["All", 2, 3], index=2
    )
    if depth == "All":
        depth = -1

    width = st.sidebar.number_input("Plot width", min_value=450, max_value=2000, value=900)
    height = st.sidebar.number_input("Plot height", min_value=450, max_value=2000)

    proportional = st.sidebar.checkbox("Make areas proportional to user count")

    st.markdown("# Treemap")

    df = pl.read_csv(DATA_DIR + DATA_FILES[dataset])
    users_df = pl.read_csv(DATA_DIR + "user_counts/" + DATA_FILES[dataset])
    hs = hr.HypothesisRow.df_to_list(df.filter(pl.col("algorithm") == algorithm), users_df)
    treemap = tm.make_treemap_from_range(
        hs, MIN_ROW, MAX_ROW, use_values=proportional, maxdepth=depth)
        #hover_data=["count"])
    treemap.update_layout(height=height, width=width, font=dict(size=FONT_SIZE))
    st.plotly_chart(treemap)


if __name__ == "__main__":
    main()

