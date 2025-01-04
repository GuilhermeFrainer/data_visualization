import pathlib
import polars as pl


class EntryBrowser:
    __DATA_PATH = pathlib.Path("data/original_datasets/")
    __MOVIE_DATA = __DATA_PATH / "MovieLens.csv"
    __BOOK_DATA = __DATA_PATH / "BookCrossing.csv"


    movie_df: pl.DataFrame
    book_df: pl.DataFrame


    def __init__(self):
        self.movie_df = pl.read_csv(EntryBrowser.__MOVIE_DATA) \
            .select(["title", "genre", "runtime_minutes", "year"]).unique("title")
        self.book_df = pl.read_csv(EntryBrowser.__BOOK_DATA).unique("book_id") \
            .select(["book_title", "book_author", "year_of_publication", "language", "category", "country"])
 

    def filter_movies(self, attributes: dict[str, str]) -> pl.DataFrame:
        df = self.movie_df
        if "year" in attributes and attributes["year"]:
            df = df.filter(pl.col("year") == attributes["year"])
        if "runtime_minutes" in attributes and attributes["runtime_minutes"]:
            df = df.filter(pl.col("runtime_minutes") == attributes["runtime_minutes"])
        if "genre" in attributes and attributes["genre"]:
            df = df.filter(pl.col("genre").str.contains(attributes["genre"]))
        return df
    

    def movie_attributes(self) -> dict[str, list[str]]:
        df = self.movie_df
        cols = [c for c in df.columns if c != "title"]
        attributes = {}

        for c in cols:
            attributes[c] = df.unique(c)[c]

        genres = set()
        for genre_list in attributes["genre"]:
            genre_iterator: list[str] = genre_list.split("|")
            for g in genre_iterator:
                genres.add(g)
        attributes["genre"] = genres
        
        return attributes
    

    def filter_books(self, attributes: dict[str, str]) -> pl.DataFrame:
        df = self.book_df
        if "year_of_publication" in attributes and attributes["year_of_publication"]:
            df = df.filter(pl.col("year_of_publication") == attributes["year_of_publication"])
        if "language" in attributes and attributes["language"]:
            df = df.filter(pl.col("language") == attributes["language"])
        if "country" in attributes and attributes["country"]:
            df = df.filter(pl.col("country") == attributes["country"])
        if "category" in attributes and attributes["category"]:
            if attributes["category"] == "body-mind-and-spirit":
                df = df.filter(pl.col("category") == "Body, Mind & Spirit")
            else:
                df = df.filter(pl.col("category") == attributes["category"])
        return df
    

    def book_attributes(self) -> dict[str, list[str]]:
        df = self.book_df.unique("book_title")
        cols = [c for c in df.columns if c != "book_title" and c != "book_author"]
        
        attributes = {}
        for c in cols:
            attributes[c] = df.unique(c)[c]
        return attributes

