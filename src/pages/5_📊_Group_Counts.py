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
    algorithm = st.sidebar.selectbox("Algorithm", [k for k in ALGORITHMS])
    side_by_side = st.sidebar.toggle("Show algorithms side-by-side")

    file = DATA_FILES[dataset]
    df = pl.read_csv(DATA_DIR / file).drop("hypothesis")

    if side_by_side:
        greedy = df.filter(pl.col("algorithm") == ALGORITHMS["Greedy"]).drop("algorithm")
        reinf = df.filter(pl.col("algorithm") == ALGORITHMS["Reinforcement Learning"]).drop("algorithm")

        cols = st.selectbox("Categories", [c for c in greedy.columns], index=None)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("## Greedy")
            fig_greedy = bar_chart.make_group_bar_chart(greedy, col=cols)
            st.plotly_chart(fig_greedy, use_container_width=True)
        
        with col2:
            st.markdown("## Reinforcement Learning")
            fig_reinf = bar_chart.make_group_bar_chart(reinf, col=cols)
            st.plotly_chart(fig_reinf, use_container_width=True)

    else:
        algorithm_name = ALGORITHMS[algorithm]
        df = df.filter(pl.col("algorithm") == algorithm_name)
        df = df.drop("algorithm")

        cols = st.selectbox("Categories", [c for c in df.columns], index=None)
        fig = bar_chart.make_group_bar_chart(df, col=cols)
        st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()

