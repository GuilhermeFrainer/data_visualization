import streamlit as st
import pathlib
import polars as pl
import pandas as pd
import seaborn as sns
from matplotlib.colors import to_hex

from hypothesis_row import HypothesisRow
from sorter import Sorter


DATA_DIR = pathlib.Path("data")
DATA_FILES = {
    "BookCrossing": "book_crossing.csv",
    "Yelp": "yelp.csv",
    "MovieLens": "movie_lens.csv",
}
USER_COUNT_DIR = DATA_DIR / "user_counts"


def main():
    st.markdown("""
        # Step Viewer
        Here you'll be able to get a better intuition of how groups are selected by the algorithm.
    """)
    
    
    dataset = st.sidebar.selectbox("Dataset", [k for k in DATA_FILES])
    file = DATA_FILES[dataset]
    original_df = pl.read_csv(DATA_DIR / file)
    user_count_df = pl.read_csv(USER_COUNT_DIR / file)
    hs = HypothesisRow.df_to_list(original_df, user_count_df)
    df = pipeline_dataframe(hs).to_pandas()

    sorting_opts = st.multiselect("Sort by", [c for c in df.columns])
    sorted_df = df.sort_values(by=sorting_opts, key=Sorter.super_sort, na_position="first")
    # Reorders columns, putting those selected by the user first
    diff = sorted_df.columns.difference(sorting_opts)
    sorted_df = sorted_df[sorting_opts + diff.to_list()]

    color_map = get_color_map_for_dataframe(df)
    
    def style_nominal_values(color_map: dict, val: str):
        return color_map.get(val, "")

    
    st.dataframe(sorted_df.style.map(lambda val: style_nominal_values(color_map, val)))


def get_color_map_for_dataframe(df: pd.DataFrame) -> dict:
    unique_values = df.stack().unique()
    palette = sns.color_palette("hsv", len(unique_values))
    color_map = {
        val: f"background-color: {to_hex(color)}"
        for val, color in zip(unique_values, palette)
    }
    return color_map


def pipeline_dataframe(hs: list[HypothesisRow]) -> pl.DataFrame:
    rows: list[dict] = []
    all_attributes = set()

    for h in hs:
        for c in h.children:
            attrs = {}
            for k, v in c.attributes.items():
                attrs[k] = v
            rows.append(attrs)
    for r in rows:
        for k in r:
            all_attributes.add(k)

    for r in rows:
        for a in all_attributes:
            if a not in r:
                r[a] = None

    return pl.DataFrame(rows)


if __name__ == "__main__":
    main()

