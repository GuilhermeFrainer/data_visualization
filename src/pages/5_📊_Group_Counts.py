import pathlib
import bar_chart
import streamlit as st
import polars as pl


DATA_DIR = pathlib.Path("data/groups")
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
    st.markdown("""
        # Group counts
        The chart below displays in how many hypothesis each label has been seen.
    """)

    dataset = st.sidebar.selectbox("Dataset", [k for k in DATA_FILES])
    file = DATA_FILES[dataset]
    df = pl.read_csv(DATA_DIR / file)

    algorithm = st.sidebar.selectbox("Algorithm", [k for k in ALGORITHMS])
    algorithm_name = ALGORITHMS[algorithm]
    df = df.filter(pl.col("algorithm") == algorithm_name)
    df = df.drop(["algorithm", "hypothesis"])

    cols = st.selectbox("Categories", [c for c in df.columns], index=None)
    fig = bar_chart.make_group_bar_chart(df, col=cols)
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()

