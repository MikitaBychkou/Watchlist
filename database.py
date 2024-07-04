from models import Film, SessionLocal

class DatabaseManager:
    def __init__(self):
        self.session = SessionLocal()

    def add_film(self, title, director, genre, status, rating, publication_year, comments):
        new_film = Film(
            title=title,
            director=director,
            genre=genre,
            status=status,
            rating=rating,
            publication_year=publication_year,
            comments=comments
        )
        self.session.add(new_film)
        self.session.commit()

    def remove_film(self, title):
        film = self.session.query(Film).filter(Film.title == title).first()
        if film:
            self.session.delete(film)
            self.session.commit()
        else:
            raise ValueError(f"Film with title '{title}' not found.")

    def edit_film(self, title, new_title=None, new_director=None, new_genre=None, new_status=None, new_rating=None,
                  new_publication_year=None, new_comments=None):
        film = self.session.query(Film).filter(Film.title == title).first()
        if film:
            if new_title:
                film.title = new_title
            if new_director:
                film.director = new_director
            if new_genre:
                film.genre = new_genre
            if new_status:
                film.status = new_status
            if new_rating is not None:
                film.rating = new_rating
            if new_publication_year is not None:
                film.publication_year = new_publication_year
            if new_comments:
                film.comments = new_comments
            self.session.commit()
        else:
            raise ValueError(f"Film with title '{title}' not found.")

    def get_all_films(self):
        return self.session.query(Film).all()

    def get_film_by_title(self, title):
        return self.session.query(Film).filter(Film.title == title).first()

    def get_watched_films(self):
        return self.session.query(Film).filter(Film.status == 'watched').all()