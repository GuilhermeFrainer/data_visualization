import pandas as pd
import re


class Sorter:
    __AGE_RANGES = {None, "<18", "18-24", "25-34", "35-44", "45-49", "50-55", ">56"}
    __RUNTIMES = {None, "Short", "Long", "Very Long"}

    @staticmethod
    def super_sort(s: pd.Series) -> pd.Series:
        def is_decade(x: str) -> bool:
            if not x or pd.isna(x):
                return True
            elif not isinstance(x, str):
                return False
            return bool(re.match(r"^\d{1,4}s$", x))

        if s.map(lambda x: x in Sorter.__AGE_RANGES).all():
            return Sorter.sort_age(s)
        # unpopular, semipopular, popular
        elif s.map(lambda x: "" if not x else x).map(lambda x: True if "popular" in x else False).any():
            return Sorter.sort_fans(s)
        # Short, Long, Very Long
        elif s.map(lambda x: x in Sorter.__RUNTIMES).all():
            return Sorter.sort_runtime(s)
        # 30s, 20s, 2000s, 1300s
        elif s.map(is_decade).all():
            return Sorter.sort_year(s)
        return s


    @staticmethod
    def sort_age(ages: pd.Series) -> pd.Series:
        return ages.map({
            None: 0,
            "<18": 1,
            "18-24": 2,
            "25-34": 3,
            "35-44": 4,
            "45-49": 5,
            "50-55": 6,
            ">56": 7
        })


    @staticmethod
    def sort_runtime(runtimes: pd.Series) -> pd.Series:
        return runtimes.map({
            None: 0,
            "Short": 1,
            "Long": 2,
            "Very Long": 3
        })


    @staticmethod
    def sort_year(years: pd.Series) -> pd.Series:
        def convert_elements(el) -> int:
            if not el or pd.isna(el):
                return 0
            n = int(el.replace("s", ""))
            if n < 100 and n != 0:
                n += 1900
            return n
        return years.map(convert_elements)
    

    @staticmethod
    def sort_fans(fans: pd.Series) -> pd.Series:
        return fans.map({
            None: 0,
            "unpopular": 1,
            "semipopular": 2,
            "popular": 3
        })
    
