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
ORIGINAL_DATASETS = DATA_DIR / "original_datasets"
ID_COL = {"BookCrossing": "book_id", "MovieLens": "item_id"}
COLUMS_OF_INTEREST = {
    "BookCrossing": ["book_title", "book_author", "year_of_publication", "language", "category"],
    "MovieLens": ["title", "genre", "year"]
}
ALGORITHMS = {
    "Greedy": "Greedy-HEP",
    "Reinforcement Learning": "RL-HEP",
}


def main():
    st.markdown("""
        # Step Viewer
        Here you'll be able to get a better intuition of how groups are selected by the algorithm.
    """)
    
    
    dataset = st.sidebar.selectbox("Dataset", [k for k in DATA_FILES])
    file = DATA_FILES[dataset]
    original_df = pl.read_csv(DATA_DIR / file)
    user_count_df = pl.read_csv(USER_COUNT_DIR / file)

    algorithm = st.sidebar.selectbox("Algorithm", [k for k in ALGORITHMS])
    algorithm_name = ALGORITHMS[algorithm]
    original_df = original_df.filter(pl.col("algorithm") == algorithm_name)

    hs = HypothesisRow.df_to_list(original_df, user_count_df)
    df = HypothesisRow.hypothesis_rows_to_group_df(hs, include_hipothesis=True).to_pandas()

    sorting_opts = st.multiselect("Sort by", [c for c in df.columns])
    sorted_df = df.sort_values(by=sorting_opts, key=Sorter.super_sort, na_position="first")
    # Reorders columns, putting those selected by the user first
    diff = sorted_df.columns.difference(sorting_opts)
    sorted_df = sorted_df[sorting_opts + diff.to_list()]

    color_map = get_color_map_for_dataframe(df)
    
    def style_nominal_values(color_map: dict, val: str):
        return color_map.get(val, "")

    
    if dataset != "Yelp":
        col1, col2 = st.columns(2)

        with col1:
            selection = st.dataframe(
                sorted_df.style.map(lambda val: style_nominal_values(color_map, val)),
                on_select="rerun",
                selection_mode="single-row",
                use_container_width=True)

        if selection["selection"]["rows"]:
            selected_row = selection["selection"]["rows"][0]
            row_attributes = sorted_df.iloc[selected_row].to_dict()

            relations_df = pl.read_csv(ORIGINAL_DATASETS / f"{dataset}.csv")
            filtered_df = relations_df
            for k, v in row_attributes.items():
                if row_attributes[k] and k != "hypothesis":
                    filtered_df = filtered_df.filter(pl.col(k) == v)
            
            filtered_df = filtered_df.unique(ID_COL[dataset]).select(COLUMS_OF_INTEREST[dataset])
            
            with col2:
                st.dataframe(filtered_df, use_container_width=True)
    else:
        st.dataframe(
            sorted_df.style.map(lambda val: style_nominal_values(color_map, val)),
            use_container_width=True)


def get_color_map_for_dataframe(df: pd.DataFrame) -> dict:
    unique_values = df.stack().unique()
    palette = sns.color_palette("hsv", len(unique_values))
    color_map = {
        val: f"background-color: {to_hex(color)}"
        for val, color in zip(unique_values, palette)
    }
    return color_map


if __name__ == "__main__":
    main()

