from datetime import datetime
from MyException import ScaleError, FilmValueError
class Film:
    """
       A class used to represent a Film.

       Attributes
       ----------
       title : str
           The title of the film.
       genre : str
           The genre of the film.
       director : str
           The director of the film.
       status : str
           The status of the film (watched/unwatched).
       rating : float
           The rating of the film (0-10).
       publication_year : int
           The year the film was published.
       comments : str, optional
           Comments about the film.
       """
    def __init__(self, title, director, genre, status, rating, publication_year, comments="No comments"):
        """
        Initializes the Film with title, director, genre, status, rating, and publication year.

        Parameters
        ----------
        title : str
            The title of the film. Must be a non-empty string.
        director : str
            The director of the film. Must be a non-empty string.
        genre : str
            The genre of the film. Must be a non-empty string.
        status : str
            The status of the film. Must be either 'watched' or 'unwatched'.
        rating : float
            The rating of the film. Must be a number between 0 and 10.
        publication_year : int
            The year the film was published. Must be an integer between 1895 and the current year.

        Raises
        ------
        ValueError
            If title, director, genre, or status are not valid strings or if status is not 'watched' or 'unwatched'.
        ScaleError
            If rating is not between 0 and 10 or if publication year is not between 1895 and the current year.
        """
        if not title or not isinstance(title, str):
            raise FilmValueError("Title cannot be empty and must be a string")
        if not director or not isinstance(director, str) or not director.replace(' ', '').isalpha():
            raise FilmValueError(
                "Director cannot be empty and must be a valid string containing only letters and spaces")
        if not genre or not isinstance(genre, str) or not genre.replace(' ', '').isalpha():
            raise FilmValueError("Genre cannot be empty and must be a valid string containing only letters and spaces")
        if not status or status.lower() not in ["watched", "unwatched"]:
            raise FilmValueError("Status must be either 'watched' or 'unwatched'")
        if not isinstance(rating, (int, float)):
            raise FilmValueError("Rating must be a number")
        if not isinstance(publication_year, int):
            raise FilmValueError("Publication year must be an integer")

        self.title = title
        self.genre = genre
        self.director = director
        self.status = status.lower()

        if not (0 <= rating <= 10):
            raise ScaleError("Rating must be between 0 and 10")
        self.rating = rating

        current_year = datetime.now().year
        if not (1895 <= publication_year <= current_year):
            raise ScaleError(f"Publication year must be between 1895 and {current_year}")
        self.publication_year = publication_year

        self.comments = "No comments"

        self.comments = comments

    def __str__(self):
        """
        Returns a string representation of the Film object.

        Returns
        -------
        str
            A string describing the film.
        """
        return (f"Film(title={self.title}, director={self.director}, genre={self.genre},"
                f" status={self.status}, rating={self.rating},"
                f" publication_year={self.publication_year}, comments={self.comments})")


