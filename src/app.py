import streamlit as st
import polars as pl
import pandas as pd

import hypothesis_row as hr
import treemap as tm


DATA_PATH = "data/rl_vs_greedy_stepwise_results.csv"


def main():
    df = pl.read_csv(DATA_PATH)
    hs = hr.HypothesisRow.df_to_list(df)
    treemap = tm.make_treemap_from_range(hs, 0, 10)
    treemap


if __name__ == "__main__":
    main()

