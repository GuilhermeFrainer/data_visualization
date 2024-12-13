import polars as pl
import plotly.graph_objects as go
import sys

from hypothesis_row import HypothesisRow


__COLORS = [
    "red",
    "green",
    "blue",
    "yellow",
    "lime",
    "maroon",
    "fuchsia",
    "olive",
    "navy",
    "purple",
    "teal",
    "aqua"
]


def make_treemap_from_range(hs: list[HypothesisRow], start: int, end: int) -> go.Figure:
    """
    Draws a treemap based on the list.

    Args:
        hs (list[HypothesisRow]): list of HypothesisRow elements.
        start (int): beginning of the range to be plotted.
        end (int): end of the range (non-inclusive).

    Returns:
        go.Figure: treemap with the hypothesis in the range drawn.
    """
    df = hs[start].get_parent_child_df()
    for h in hs[start + 1:end]:
        df = __add_subroot_to_df(df, h)

    fig = go.Figure()
    fig.add_trace(
        go.Treemap(
            ids=df["child"],
            parents=df["parent"],
            labels=df["label"],
        )
    )
    return fig


def __add_subroot_to_df(df: pl.DataFrame, subroot: HypothesisRow) -> pl.DataFrame:
    """
    Adds subroot to parent-child DataFrame

    Args:
        df (pl.DataFrame): pre-existing parent-child DataFrame
        subroot (HypothesisRow): new HypothesisRow to add

    Returns:
        pl.DataFrame: DataFrame with the added subroot
    """
    subroot_df = subroot.get_parent_child_df()
    subroot_name = subroot_df["child"][0]
    filtered_df = df.filter(pl.col("child") == subroot_name)
    if len(filtered_df) == 0:
        return pl.concat([df, subroot_df])
    else:
        return pl.concat([df, subroot_df[1:]])


def __get_treemap_colors(hs: pl.Series) -> dict[str, str]:
    """
    Creates color list to be used when drawing the treemap.
    Each color represents one hypothesis.

    Args:
        hs (pl.Series): series of hypotheses (str)

    Returns:
        list[str]: List of colors
    """
    color_map = {}
    color_idx = 0
    for h in hs:
        if h not in color_map:
            try:
                color_map[h] = __COLORS[color_idx]
                color_idx += 1
            except IndexError:
                sys.exit("Insufficient colors for the number of hypotheses present.")
    return [color_map[h] for h in hs]

