import polars as pl
import sys

from polars.exceptions import ColumnNotFoundError


class Group:
    attributes: dict[str, str]
    count: int

    def __init__(self, s: str, df: pl.DataFrame):
        self.attributes = Group.__attributes_from_str(s)
        self.count = Group.__get_user_count(df, self.attributes)


    @staticmethod
    def groups_from_row(s: str, df: pl.DataFrame) -> list[dict[str, str]]:
        """
        Creates groups from the value in the "G_out" column.

        Args:
            s (str): string value from a G_out column representing all groups outputted.
            df (pl.DataFrame): users dataframe.

        Returns:
            list[dict[str, str]]: list of attribute dictionaries, one for each group.
        """
        if not s:
            return []
        # Quickie fix
        s = s.replace("Body, Mind & Spirit", "body-mind-and-spirit")
        groups = s.split(",")
        return [Group(g, df) for g in groups]
    

    def to_string(self) -> str:
        """
        Converts group attribute dictionary into string.

        Returns:
            str: string representing group's attributes.
        """
        out_str = ""
        for k, v in sorted(self.attributes.items()):
            try:
                out_str += k + ":" + v + ","
            except TypeError:
                sys.exit(f"Key: {k}, value: {v}")
        return out_str[:-1].strip()


    # ---------------- #
    # HELPER FUNCTIONS #
    # ---------------- #

    @staticmethod
    def __attributes_from_str(s: str) -> dict[str, str]:
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
                attr_dict[k.strip()] = v.strip()
            except ValueError:
                if a == "All users":
                    attr_dict["all_users"] = "all"
                else:
                    raise ValueError("Couldn't unpack value: " + a)
        return attr_dict
    

    @staticmethod
    def __get_user_count(df: pl.DataFrame, attributes: dict[str, str]) -> int:
        """
        Gets user count for a certain group.

        Args:
            df (pl.DataFrame): DataFrame containing unique users.
            
            attributes (dict[str, str]): Group's attribute dictionary.

        Returns:
            int: user count for that group.
        """
        filtered_df = df
        for k, v in attributes.items():
            try: 
                filtered_df = filtered_df.filter(pl.col(k) == v)
            except ColumnNotFoundError:
                continue
        return len(filtered_df)
    
