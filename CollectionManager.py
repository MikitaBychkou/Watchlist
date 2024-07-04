from database import DatabaseManager
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from MyException import FilmValueError, ScaleError

class CollectionManager:
    def __init__(self):
        self.db = DatabaseManager()
        self.watched_history = []

    def add_film(self, title, director, genre, status, rating, publication_year, comments="No comments"):
        self.db.add_film(title, director, genre, status, rating, publication_year, comments)
        if status == "watched":
            self.watched_history.append((title, datetime.now().strftime("%d-%m-%Y")))

    def remove_film(self, title):
        self.db.remove_film(title)

    def edit_film(self, title, new_title=None, new_director=None, new_genre=None, new_status=None, new_rating=None,
                  new_publication_year=None, new_comments=None):
        self.db.edit_film(title, new_title, new_director, new_genre, new_status, new_rating, new_publication_year, new_comments)
        if new_status == "watched":
            self.watched_history.append((new_title if new_title else title, datetime.now().strftime("%d-%m-%Y")))
        elif new_status == "unwatched":
            self.watched_history = [(t, d) for t, d in self.watched_history if t != title]

    def edit_status_film(self, title, new_status):
        self.db.edit_film(title, new_status=new_status)
        if new_status == "watched":
            self.watched_history.append((title, datetime.now().strftime("%d-%m-%Y")))
        elif new_status == "unwatched":
            self.watched_history = [(t, d) for t, d in self.watched_history if t != title]

    def rate_film(self, title, rating):
        self.edit_film(title, new_rating=rating)

    def comment_film(self, title, comment):
        self.edit_film(title, new_comments=comment)

    def search_films(self, title=None, genre=None, director=None, rating=None, publication_year=None):
        results = []
        for film in self.db.get_all_films():
            if (title and title.lower() in film.title.lower()) or \
               (genre and genre.lower() in film.genre.lower()) or \
               (director and director.lower() in film.director.lower()) or \
               (rating is not None and rating == film.rating) or \
               (publication_year and publication_year == film.publication_year):
                results.append(film)
        return results

    def view_collection(self):
        films = self.db.get_all_films()
        return films

    def view_film(self, title):
        return self.db.get_film_by_title(title)

    def view_watched_history(self):
        return self.db.get_watched_films()

    def generate_statistics(self):
        films = self.db.get_all_films()
        if not films:
            return {
                "total_films": 0,
                "genre_count": {},
                "average_rating": 0,
                "watched_count": 0,
                "unwatched_count": 0,
                "most_watched_genre": None
            }

        df = pd.DataFrame([film.__dict__ for film in films])

        genre_count = df['genre'].value_counts().to_dict()
        average_rating = df['rating'].mean()
        watched_count = df[df['status'] == 'watched'].shape[0]
        unwatched_count = df[df['status'] == 'unwatched'].shape[0]
        most_watched_genre = df[df['status'] == 'watched']['genre'].mode()[0] if watched_count > 0 else None

        stats = {
            "total_films": len(films),
            "genre_count": genre_count,
            "average_rating": average_rating,
            "watched_count": watched_count,
            "unwatched_count": unwatched_count,
            "most_watched_genre": most_watched_genre
        }

        plt.figure(figsize=(12, 8))

        plt.subplot(2, 2, 1)
        plt.bar(stats['genre_count'].keys(), stats['genre_count'].values())
        plt.title('Number of Films by Genre')
        plt.xlabel('Genre')
        plt.ylabel('Count')

        plt.subplot(2, 2, 2)
        plt.bar(['Average Rating'], [stats['average_rating']])
        plt.title('Average Rating of Films')
        plt.ylim(0, 10)

        plt.subplot(2, 2, 3)
        plt.bar(['Watched', 'Unwatched'], [stats['watched_count'], stats['unwatched_count']])
        plt.title('Watched vs Unwatched Films')
        plt.xlabel('Status')
        plt.ylabel('Count')

        plt.subplot(2, 2, 4)
        if stats['most_watched_genre']:
            plt.bar([stats['most_watched_genre']], [stats['genre_count'][stats['most_watched_genre']]])
            plt.title('Most Watched Genre')
            plt.xlabel('Genre')
            plt.ylabel('Count')
        else:
            plt.bar(['None'], [0])
            plt.title('Most Watched Genre')
            plt.xlabel('Genre')
            plt.ylabel('Count')

        plt.tight_layout()
        plt.show()

        return stats

    def export_collection_to_file(self, file_path="collection.txt"):
        films = self.db.get_all_films()
        with open(file_path, 'w') as file:
            for film in films:
                file.write(f"Title: {film.title}\n")
                file.write(f"Director: {film.director}\n")
                file.write(f"Genre: {film.genre}\n")
                file.write(f"Status: {film.status}\n")
                file.write(f"Rating: {film.rating}\n")
                file.write(f"Publication Year: {film.publication_year}\n")
                file.write(f"Comments: {film.comments}\n")
                file.write("\n")

    def import_collection_from_file(self, file_path="collection.txt"):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                film_data = {}
                for line in lines:
                    if line.strip():
                        key, value = line.strip().split(": ", 1)
                        film_data[key.lower().replace(" ", "_")] = value
                    else:
                        try:
                            comments = film_data.get("comments", "No comments")
                            self.add_film(
                                film_data["title"],
                                film_data["director"],
                                film_data["genre"],
                                film_data["status"],
                                float(film_data["rating"]),
                                int(film_data["publication_year"]),
                                comments
                            )
                        except (ValueError, ScaleError, FilmValueError) as e:
                            print(f"Error importing film: {e}")
                        film_data = {}

                if film_data:
                    try:
                        comments = film_data.get("comments", "No comments")
                        self.add_film(
                            film_data["title"],
                            film_data["director"],
                            film_data["genre"],
                            film_data["status"],
                            float(film_data["rating"]),
                            int(film_data["publication_year"]),
                            comments
                        )
                    except (ValueError, ScaleError, FilmValueError) as e:
                        print(f"Error importing film: {e}")

        except FileNotFoundError:
            print(f"File {file_path} not found.")
        except Exception as e:
            print(f"An error occurred while importing collection: {e}")