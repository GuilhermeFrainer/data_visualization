import polars as pl
import plotly.express as px
import plotly.graph_objects as go


def make_group_bar_chart(df: pl.DataFrame, col: str | None=None, descending=True, horizontal=True) -> go.Figure:
    if col:
        counts = df[col].value_counts().drop_nulls()
        if horizontal:
            fig = px.bar(counts.sort(by="count", descending=(not descending)), x="count", y=col, orientation="h")
        else:
            fig = px.bar(counts.sort(by="count", descending=descending), x=col, y="count")
    else:
        counts = __all_counts(df).drop_nulls()
        if horizontal:
            fig = px.bar(counts, x="count", y="label", color="category", orientation="h")
            fig.update_layout(xaxis=dict(range=[0, max(counts["count"])]))
        else:
            fig = px.bar(counts, x="label", y="count", color="category")
    return fig


def __all_counts(df: pl.DataFrame) -> pl.DataFrame:
    rows = []
    for c in df.columns:
        counts = df[c].value_counts()
        for label, value in counts.iter_rows():
            rows.append({"category": c, "label": label, "count": value})
    return pl.DataFrame(rows)

