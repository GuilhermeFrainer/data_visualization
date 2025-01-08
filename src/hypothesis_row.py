import polars as pl
import plotly.graph_objects
import plotly.express as px

from group import Group


class HypothesisRow:
    algorithm: str
    step: int
    parent: Group
    hypothesis: str
    children: list[Group]
    coverage: float
    diversity: float
    normalized_diversity: float


    def __init__(self, row: tuple, users_df: pl.DataFrame):
        self.algorithm = row[0]
        self.step = row[1]
        self.parent = Group(row[2], users_df)
        if isinstance(self.parent, str):
            raise ValueError("Parent initialized as str")
        self.hypothesis = row[3]
        self.children = Group.groups_from_row(row[4], users_df)
        self.coverage = row[5]
        self.diversity = row[6]
        self.normalized_diversity = row[7]
    

    @staticmethod
    def df_to_list(df: pl.DataFrame, users_df: pl.DataFrame) -> list["HypothesisRow"]:
        return [HypothesisRow(r, users_df) for r in df.iter_rows()]


    def parent_to_string(self) -> str:
        return self.parent.to_string()
    

    def children_to_strings(self) -> list[str]:
        return [c.to_string() for c in self.children]
    

    def treemap(self) -> plotly.graph_objects.Figure:
        names = [c for c in self.children_to_strings()]
        parents = [self.parent_to_string() for _ in names]
        return px.treemap(names=names, parents=parents)
    

    def get_parent_child_df(self) -> pl.DataFrame:
        """
        Returns DataFrame with parent-child pairs in each row.

        Returns:
            pl.DataFrame: DataFrame representing parent-child relationship.
        """
        out_list = []
        out_list.append({
            "parent": "",
            "child": self.parent.to_string(),
            "label": HypothesisRow.__get_label_for_parent(self.parent),
            "hypothesis": self.hypothesis,
            "count": self.parent.count
        })
        for c in self.children:
            out_list.append({
                "parent": self.parent.to_string(),
                "child": c.to_string(),
                "label": HypothesisRow.__get_label_for_child(self.parent, c),
                "hypothesis": self.hypothesis,
                "count": c.count
            })
        return pl.DataFrame(out_list)
    

    @staticmethod
    def hypothesis_rows_to_group_df(hs: list["HypothesisRow"]) -> pl.DataFrame:
        rows: list[dict] = []
        all_attributes = set()

        for h in hs:
            for c in h.children:
                attrs = {}
                for k, v in c.attributes.items():
                    attrs[k] = v
                rows.append(attrs)
        for r in rows:
            for k in r:
                all_attributes.add(k)

        for r in rows:
            for a in all_attributes:
                if a not in r:
                    r[a] = None
        return pl.DataFrame(rows)


    # ---------------- #
    # HELPER FUNCTIONS #
    # ---------------- #


    @staticmethod
    def __get_label_for_parent(p: Group) -> str:
        """
        Creates label for parent group.

        Args:
            p (Group): parent group.

        Returns:
            str: Parent group label.
        """
        label = ""
        for _, v in p.attributes.items():
            label = v + ", "
        return label[:-2]


    @staticmethod
    def __get_label_for_child(parent: Group, c: Group) -> str:
        """
        Removes parent attributes from child string.
        Also removes key from attribute key:value pairs.
        The label will be the characteristic that differentiates the child from the parent

        Args:
            parent (Group): parent group.
            c (Group): child group.

        Returns:
            str: attribute that differentiates child group from parent group.
        """
        if isinstance(parent, str):
            raise ValueError("Parent is string: " + parent)
        for k in c.attributes:
                if k not in parent.attributes:
                    return c.attributes[k]
        raise ValueError("No attribute differentiates child from parent.")

