class Movie:
    def __init__(self, id, title, director, actors, year, average_rating):
        self.id = id
        self.title = title
        self.director = director
        self.actors = actors
        self.year = year
        self.average_rating = average_rating

    def __str__(self):
        # This is what will be displayed in the Listbox
        return f"{self.title} ({self.year})"
