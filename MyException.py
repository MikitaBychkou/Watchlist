class ScaleError(Exception):
    """Raised when the rating is out of the acceptable range (0-10)."""
    pass

class MovieNotFoundError(Exception):
    """Raised when a movie is not found in the collection."""
    pass

class FilmValueError(Exception):
    """Raised if the movie wasn't made properly."""
    pass