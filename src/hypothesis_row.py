import polars as pl
import plotly.graph_objects
import plotly.express as px
import sys


class HypothesisRow:
    algorithm: str
    step: int
    parent: dict[str, str]
    hypothesis: str
    children: list[dict[str, str]]
    coverage: float
    diversity: float
    normalized_diversity: float


    def __init__(self, row: tuple):
        self.algorithm = row[0]
        self.step = row[1]
        self.parent = HypothesisRow.group_from_str(row[2])
        self.hypothesis = row[3]
        self.children = HypothesisRow.groups_from_row(row[4])
        self.coverage = row[5]
        self.diversity = row[6]
        self.normalized_diversity = row[7]


    @staticmethod
    def group_from_str(s: str) -> dict[str, str]:
        """
        Creates group attribute dictionary given a string.

        Args:
            s (str): string cointaining attribute key:value pairs
            separated by "|".

        Returns:
            dict[str, str]: dictionary containing said attributes as key:value pairs.
        """
        attributes = s.split("|")
        attr_dict = {}
        for a in attributes:
            try:
                k, v = a.split(":")
                attr_dict[k] = v
            except ValueError:
                if a == "All users":
                    attr_dict["all_users"] = "all"
                else:
                    sys.exit("Couldn't unpack value: " + a)
        return attr_dict


    @staticmethod
    def groups_from_row(s: str) -> list[dict[str, str]]:
        """
        Creates groups from the value in the "G_out" column.

        Args:
            s (str): string value from a G_out column representing all groups outputted.

        Returns:
            list[dict[str, str]]: list of attribute dictionaries, one for each group.
        """
        if not s:
            return []
        # Quickie fix
        s = s.replace("Body, Mind & Spirit", "body-mind-and-spirit")
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
    

    # Returns a (parent, child) DataFrame
    def get_parent_child_df(self) -> pl.DataFrame:
        """
        Returns DataFrame with parent-child pairs in each row.

        Returns:
            pl.DataFrame: DataFrame representing parent-child relationship.
        """
        out_list = []
        out_list.append({"parent": "", "child": self.parent_to_string()})
        for c in self.children_to_strings():
            out_list.append({"parent": self.parent_to_string(), "child": c})
        return pl.DataFrame(out_list)


# Converts dictionary containing characteristics into string
def dict_to_string(d: dict) -> str:
    out_str = ""
    for k, v in sorted(d.items()):
        try:
            out_str += k + ":" + v + ","
        except TypeError:
            sys.exit(f"Key: {k}, value: {v}")
    return out_str[:-1].strip()

