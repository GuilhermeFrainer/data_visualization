import streamlit as st

def main():
    st.set_page_config(
        page_title="Welcome",
        page_icon="👋"
    )

    st.markdown(
        """
        # Welcome
        This project was made for the Visual Analytics for Data Science (CMP273)
        course at the Federal University of Rio Grande do Sul (UFRGS),
        ministered by professor João Luiz Dihl Comba.

        # Purpose
        Our intention here is to analyze data from multiple hypothesis generation research
        over review datasets (BookCrossing, Yelp and MovieLens).

        This is a difficult problem, since we are dealing with two multidimensional entities
        (reviewer and reviewed entity) in an N:N relationship.

        Our code is open source and available [here](https://github.com/GuilhermeFrainer/data_visualization).
        """
    )


if __name__ == "__main__":
    main()

