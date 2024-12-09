import streamlit as st
import polars as pl

import hypothesis_row as hr
import treemap as tm


DATA_DIR = "data/"
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

    df = pl.read_csv(DATA_DIR + DATA_FILES[dataset])
    filtered_df = df.filter(pl.col("algorithm") == algorithm)
    hs = hr.HypothesisRow.df_to_list(filtered_df)
    treemap = tm.make_treemap_from_range(hs, 0, 20)

    option = st.sidebar.selectbox("How do you want to visualize it?", ["Treemap", "Data frame"])
    if option == "Data frame":
        filtered_df
    elif option == "Treemap":
        treemap


if __name__ == "__main__":
    main()

