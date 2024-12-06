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


def main():
    dataset = st.sidebar.selectbox("Dataset", [k for k in DATA_FILES])

    df = pl.read_csv(DATA_DIR + DATA_FILES[dataset])
    hs = hr.HypothesisRow.df_to_list(df)
    treemap = tm.make_treemap_from_range(hs, 0, 20)

    # TODO: The prompt here could be better
    option = st.sidebar.selectbox("How to visualize it?", ["Treemap", "Data frame"])
    if option == "Data frame":
        df
    elif option == "Treemap":
        treemap


if __name__ == "__main__":
    main()

