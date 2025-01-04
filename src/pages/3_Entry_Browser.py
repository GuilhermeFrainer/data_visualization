import streamlit as st
from entry_browser import EntryBrowser


DATASETS = {"Movies", "Books"}


def main():
    st.markdown("""
    # Entry browser
                
    This page allows you to browse through the movies and books in the datasets used here.
    """)

    entry_browser = EntryBrowser()

    dataset = st.sidebar.selectbox("Data", DATASETS)

    if dataset == "Books":
        selection = {}
        for k, v in entry_browser.book_attributes().items():
            selection[k] = st.selectbox(k, sorted(v), index=None)

        df = entry_browser.filter_books(selection)
        df

    elif dataset == "Movies":
        selection = {}
        for k, v in entry_browser.movie_attributes().items():
            selection[k] = st.selectbox(k, sorted(v), index=None)

        df = entry_browser.filter_movies(selection)
        df


if __name__ == "__main__":
    main()

