import pathlib
import bar_chart
import streamlit as st
import polars as pl

from hypothesis_row import HypothesisRow


DATA_DIR = pathlib.Path("data")
DATA_FILES = {
    "BookCrossing": "book_crossing.csv",
    "Yelp": "yelp.csv",
    "MovieLens": "movie_lens.csv",
}
USER_COUNT_DIR = DATA_DIR / "user_counts"
ALGORITHMS = {
    "Greedy": "Greedy-HEP",
    "Reinforcement Learning": "RL-HEP",
}


def main():
    st.markdown("""
        # Group counts
        The chart below displays in how many hypothesis each label has been seen.
    """)

    dataset = st.sidebar.selectbox("Dataset", [k for k in DATA_FILES])
    file = DATA_FILES[dataset]
    original_df = pl.read_csv(DATA_DIR / file)
    user_count_df = pl.read_csv(USER_COUNT_DIR / file)

    algorithm = st.sidebar.selectbox("Algorithm", [k for k in ALGORITHMS])
    algorithm_name = ALGORITHMS[algorithm]
    original_df = original_df.filter(pl.col("algorithm") == algorithm_name)

    hs = HypothesisRow.df_to_list(original_df, user_count_df)
    df = HypothesisRow.hypothesis_rows_to_group_df(hs)

    cols = st.selectbox("Categories", [c for c in df.columns], index=None)
    fig = bar_chart.make_group_bar_chart(df, col=cols)
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()

