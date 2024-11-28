import polars as pl
import plotly.graph_objects
import plotly.express as px


class HypothesisRow:
    algorithm: str
    n: int
    parent: dict[str, str]
    hypothesis: str
    children: list[dict[str, str]]
    coverage: float
    diversity: float
    power: float
    fdr: float
    time: float


    def __init__(self, row: tuple):
        self.algorithm = row[0]
        self.n = row[1]
        self.parent = HypothesisRow.group_from_str(row[2])
        self.hypothesis = row[3]
        self.children = HypothesisRow.groups_from_row(row[4])
        self.coverage = row[5]
        self.diversity = row[6]
        self.power = row[7]
        self.fdr = row[8]
        self.time = row[9]


    @staticmethod
    def group_from_str(s: str) -> dict[str, str]:
        attributes = s.split("|")
        attr_dict = {}
        for a in attributes:
            k, v = a.split(":")
            attr_dict[k] = v
        return attr_dict


    @staticmethod
    def groups_from_row(s: str) -> list[dict[str, str]]:
        groups = s.split(",")
        return [HypothesisRow.group_from_str(g) for g in groups]
    

    @staticmethod
    def df_to_list(df: pl.DataFrame) -> list["HypothesisRow"]:
        return [HypothesisRow(r) for r in df.iter_rows()]


    def parent_to_string(self) -> str:
        return dict_to_string(self.parent)
    

    def children_to_strings(self) -> list[str]:
        return [dict_to_string(c) for c in self.children]
    

    def treemap(self) -> plotly.graph_objects.Figure:
        names = [c for c in self.children_to_strings()]
        parents = [self.parent_to_string() for _ in names]
        return px.treemap(names=names, parents=parents)


# Converts dictionary containing characteristics into string
def dict_to_string(d: dict) -> str:
    out_str = ""
    for k, v in d.items():
        out_str += k + ":" + v + ","
    return out_str[:-1]

