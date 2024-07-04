from CollectionManager import CollectionManager
from MyException import MovieNotFoundError, ScaleError, FilmValueError

class Main:
    """
    A class that provides a console interface for managing a film collection.

    Attributes
    ----------
    manager : CollectionManager
        An instance of CollectionManager to manage the film collection.
    options : dict
        A dictionary mapping user input options to corresponding methods.
    """

    def __init__(self):
        """
        Initializes the Main class with a CollectionManager instance and menu options.
        """
        self.manager = CollectionManager()
        self.options = {
            "1": self.add_film,
            "2": self.edit_film,
            "3": self.rate_film,
            "4": self.comment_film,
            "5": self.search_films,
            "6": self.view_collection,
            "7": self.export_collection,
            "8": self.view_watched_history,
            "9": self.generate_statistics,
            "10": self.remove_film,
            "11": self.view_film,
            "12": self.edit_status_film,
            "13": self.import_collection,
            "0": self.exit
        }

    def display_menu(self):
        """
        Displays the menu options to the user.
        """
        print("""
        Collection Manager
        1. Add a new film
        2. Edit a film
        3. Rate a film
        4. Comment on a film
        5. Search for films
        6. View collection
        7. Export collection to file
        8. View watched history
        9. Generate statistics
        10. Remove a film
        11. View a film
        12. Edit a film's status
        13. Import collection from file
        0. Exit
        """)

    def run(self):
        """
        Runs the main loop to accept and process user input.

        Raises
    ------
    ValueError
        If the user input cannot be converted to the required type.
    ScaleError
        If the rating or publication year provided is out of the acceptable range.
    FilmValueError
        If the film attributes (title, director, genre, status) are invalid.
    MovieNotFoundError
        If the film to be edited or removed is not found in the collection.
        """
        while True:
            self.display_menu()
            choice = input("Enter an option: ")
            action = self.options.get(choice)
            if action:
                try:
                    action()
                except (ValueError, ScaleError, FilmValueError, MovieNotFoundError) as e:
                    print(f"Error: {e}")
            else:
                print(f"{choice} is not a valid choice")

    def add_film(self):
        """
        Prompts the user to add a new film to the collection.
        """
        title = input("Enter title: ")
        director = input("Enter director: ")
        if not director.replace(' ', '').isalpha():
            raise FilmValueError("Director must be a valid string containing only letters and spaces")
        genre = input("Enter genre: ")
        if not genre.replace(' ', '').isalpha():
            raise FilmValueError("Genre must be a valid string containing only letters and spaces")
        status = input("Enter status (watched/unwatched): ")
        rating = float(input("Enter rating (0-10): "))
        publication_year = int(input("Enter publication year: "))
        self.manager.add_film(title, director, genre, status, rating, publication_year)

    def edit_film(self):
        """
        Prompts the user to edit an existing film's information.
        """
        title = input("Enter the title of the film to edit: ")
        new_title = input("Enter new title (leave blank to keep current): ")
        new_director = input("Enter new director (leave blank to keep current): ")
        if new_director and not new_director.replace(' ', '').isalpha():
            raise FilmValueError("Director must be a valid string containing only letters and spaces")
        new_genre = input("Enter new genre (leave blank to keep current): ")
        if new_genre and not new_genre.replace(' ', '').isalpha():
            raise FilmValueError("Genre must be a valid string containing only letters and spaces")
        new_status = input("Enter new status (watched/unwatched, leave blank to keep current): ")
        new_rating = input("Enter new rating (0-10, leave blank to keep current): ")
        new_publication_year = input("Enter new publication year (leave blank to keep current): ")

        self.manager.edit_film(
            title,
            new_title if new_title else None,
            new_director if new_director else None,
            new_genre if new_genre else None,
            new_status if new_status else None,
            float(new_rating) if new_rating else None,
            int(new_publication_year) if new_publication_year else None
        )

    def rate_film(self):
        """
        Prompts the user to rate a film.
        """
        title = input("Enter the title of the film to rate: ")
        rating = float(input("Enter rating (0-10): "))
        self.manager.rate_film(title, rating)

    def edit_status_film(self):
        """
        Prompts the user to edit a film's status.
        """
        title = input("Enter the title of the film to edit status: ")
        status = input("Enter new status (watched/unwatched): ")
        self.manager.edit_status_film(title, status)

    def comment_film(self):
        """
        Prompts the user to add a comment to a film.
        """
        title = input("Enter the title of the film to comment on: ")
        comment = input("Enter your comment: ")
        self.manager.comment_film(title, comment)

    def search_films(self):
        """
        Prompts the user to search for films based on various criteria.
        """
        title = input("Enter title to search (leave blank to skip): ")
        genre = input("Enter genre to search (leave blank to skip): ")
        director = input("Enter director to search (leave blank to skip): ")
        rating = input("Enter rating to search (leave blank to skip): ")
        publication_year = input("Enter publication year to search (leave blank to skip): ")

        results = self.manager.search_films(
            title if title else None,
            genre if genre else None,
            director if director else None,
            float(rating) if rating else None,
            int(publication_year) if publication_year else None
        )

        if not results:
            print("No films found.")
        else:
            for film in results:
                print(film)

    def view_collection(self):
        """
        Displays the titles of all films in the collection.
        """
        films = self.manager.view_collection()
        for film in films:
            print(f"Title: {film.title}, Director: {film.director}, Genre: {film.genre}, Status: {film.status}, Rating: {film.rating}, Publication Year: {film.publication_year}, Comments: {film.comments}")
    def export_collection(self):
        """
        Prompts the user to specify a file path to export the collection.
        """
        file_path = input("Enter file path to export collection: ")
        if file_path == '':
            file_path = 'collection.txt'
        self.manager.export_collection_to_file(file_path)
        print(f"Collection exported to {file_path}")

    def import_collection(self):
        """
        Prompts the user to import a collection from a file.
        """
        file_path = input("Enter file path to import collection: ")
        if file_path == '':
            file_path = 'collection.txt'
        try:
            self.manager.import_collection_from_file(file_path)
            print(f"Collection imported from {file_path}")
        except Exception as e:
            print(f"Error importing collection: {e}")

    def view_watched_history(self):
        """
        Displays the history of watched films.
        """
        watched_films = self.manager.view_watched_history()
        for film in watched_films:
            print(f"Title: {film.title}, Director: {film.director}, Genre: {film.genre}, Rating: {film.rating}, Publication Year: {film.publication_year}, Comments: {film.comments}")

    def generate_statistics(self):
        """
        Generates and displays statistics about the film collection.
        """
        stats = self.manager.generate_statistics()
        print("Total Films:", stats["total_films"])
        print("Genre Count:", stats["genre_count"])
        print("Average Rating:", stats["average_rating"])
        print("Watched Count:", stats["watched_count"])
        print("Unwatched Count:", stats["unwatched_count"])
        print("Most Watched Genre:", stats["most_watched_genre"])

    def remove_film(self):
        """
        Prompts the user to remove a film from the collection.
        """
        title = input("Enter the title of the film to remove: ")
        try:
            self.manager.remove_film(title)
            print(f"Film '{title}' removed from the collection.")
        except MovieNotFoundError as e:
            print(e)

    def view_film(self):
        """
        Prompts the user to view a film from the collection.
        """
        title = input("Enter the title of the film to view: ")
        try:
            film = self.manager.view_film(title)
            if film:
                print(f"Title: {film.title}\nDirector: {film.director}\nGenre: {film.genre}\nStatus: {film.status}\nRating: {film.rating}\nPublication Year: {film.publication_year}\nComments: {film.comments}")
            else:
                print(f"Film with title '{title}' not found.")
        except MovieNotFoundError as e:
            print(e)

    def exit(self):
        """
        Exits the program.
        """
        print("Exit from the program.")
        exit()


Main().run()
