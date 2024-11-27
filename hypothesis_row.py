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
    
