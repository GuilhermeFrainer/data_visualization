import streamlit as st
import polars as pl

import hypothesis_row as hr


DATA_DIR = "data/"
DATA_FILES = {
    "BookCrossing": "book_crossing.csv",
    "Yelp": "yelp.csv",
    "MovieLens": "movie_lens.csv",
}


def main():
    dataset_options = [k for k in DATA_FILES]
    dataset = st.sidebar.selectbox("Dataset", dataset_options)
    df = pl.read_csv(DATA_DIR + DATA_FILES[dataset])

    columns = st.sidebar.multiselect(
        "Columns to display",
        df.columns,
        df.columns
    )
    filtered_df = df.select(columns)
    filtered_df

if __name__ == "__main__":
    main()

