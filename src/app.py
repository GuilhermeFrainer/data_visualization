import streamlit as st
import polars as pl

import hypothesis_row as hr
import treemap as tm


DATA_DIR = "data/"
MIN_ROW = 0
MAX_ROW = 35
DATA_FILES = {
    "BookCrossing": "book_crossing.csv",
    "Yelp": "yelp.csv",
    "MovieLens": "movie_lens.csv",
}
ALGORITHMS = {
    "Greedy": "Greedy-HEP",
    "Reinforcement Learning": "RL-HEP",
}


def main():
    dataset_options = [k for k in DATA_FILES]
    algo_options = [k for k in ALGORITHMS]

    dataset = st.sidebar.selectbox("Dataset", dataset_options)
    algorithm = ALGORITHMS[st.sidebar.selectbox("Algorithm", algo_options)]
    rows_to_display = st.sidebar.number_input(
        "Rows to display", min_value=MIN_ROW + 1, max_value=MAX_ROW)

    df = pl.read_csv(DATA_DIR + DATA_FILES[dataset])
    filtered_df = df.filter(pl.col("algorithm") == algorithm) \
        .filter(pl.col("step") < rows_to_display)
    hs = hr.HypothesisRow.df_to_list(filtered_df)
    treemap = tm.make_treemap_from_range(hs, MIN_ROW, rows_to_display)

    option = st.sidebar.selectbox("How do you want to visualize it?", ["Treemap", "Data frame"])
    if option == "Data frame":
        filtered_df
    elif option == "Treemap":
        treemap


if __name__ == "__main__":
    main()

