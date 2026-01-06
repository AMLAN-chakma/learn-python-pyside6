# Toggle on and off to see debug output
debug = True
class MediaError(Exception):
    """Custom exception for media-related errors."""
    def __init__(self, message, obj):
        super().__init__(message)
        self.obj = obj

class Movie:
    def __init__(self, title, year, director, duration):
        """ Initialize a Movie object with validation."""
        # Type checks
        if not isinstance(title, str):
            raise ValueError("Title must be a string")
        if not isinstance(director, str):
            raise ValueError("Director must be a string")

        # Value checks
        if not title.strip():
            raise ValueError("Title cannot be empty")
        if year < 1895:
            raise ValueError("Year must be 1895 or later")
        if not director.strip():
            raise ValueError("Director cannot be empty")
        if not any(char.isalpha() for char in director):
            raise ValueError("Director must contain at least one letter")
        if duration <= 0:
            raise ValueError("Duration must be positive")

        self.title = title
        self.year = year
        self.director = director
        self.duration = duration

    def __str__(self):
        return f'{self.title} ({self.year}) - {self.duration} min, {self.director}'

class MediaCatalogue:
    """Manage a collection of media items."""
    def __init__(self):
        self.items = []

    def add(self, media_item):
        """Add a media item to the catalogue."""
        if not isinstance(media_item, Movie):
            raise MediaError('Only Movie or TVSeries instances can be added', media_item)
        self.items.append(media_item)
        return media_item

    def delete(self, media_item):
        """Delete a media item from the catalogue."""
        if media_item not in self.items:
            raise MediaError('Item not found in catalogue', media_item)
        self.items.remove(media_item)
        return media_item

    def get_movies(self):
        """Return a list of just theMovie instances in the catalogue."""
        return [item for item in self.items if type(item) is Movie]

    def get_tv_series(self):
        """Return a list of just the TVSeries instances in the catalogue."""
        return [item for item in self.items if type(item) is TVSeries]
    
    def filter_by_series_or_movie(self, type):
        """Return a list of just the Movie or TVSeries instances in the catalogue."""
        if type == 'movie':
            return self.get_movies()
        elif type == 'series':
            return self.get_tv_series()
        else:
            raise ValueError('Invalid type. Must be "movie" or "series"')
    
    def __str__(self):
        if not self.items:
            return "Media Catalogue (empty)"
        movies = self.get_movies()
        series = self.get_tv_series()
        result = f'Media Catalogue ({len(self.items)} items):\n\n'

        if movies:
            result += "=== MOVIES ===\n"
            for i, movie in enumerate(movies, 1):
               result += f"{i}. {movie}\n"
        if series:
            result += "\n=== TV SERIES ===\n"
            for i, series in enumerate(series, 1):
                result += f"{i}. {series}\n"
        return result

class TVSeries(Movie):
    def __init__(self,title,year,director,duration,seasons,total_episodes):
        super().__init__(title,year,director,duration)

        if seasons  < 1:
            raise ValueError("Seasons must be 1 or greater")

        if total_episodes < 1:
            raise ValueError("Total episodes must be 1 or greater")

        self.seasons = seasons
        self.total_episodes = total_episodes

    def __str__(self):
        """ Override the __str__ method to provide a string representation of the TVSeries object."""
        return f"{self.title} ({self.year}) - {self.seasons} seasons, {self.total_episodes} episodes, {self.duration} min avg, {self.director}"


if __name__ == "__main__" and debug == True:
    catalogue = MediaCatalogue()
    try:
        movie1 = Movie('The Matrix', 1999, 'The Wachowskis', 136)
        catalogue.add(movie1)
        movie2 = Movie('Inception', 2010, 'Christopher Nolan', 148)
        catalogue.add(movie2)

        series1 = TVSeries('Scrubs', 2001, 'Bill Lawrence', 24, 9, 182)
        catalogue.add(series1)
        series2 = TVSeries('Breaking Bad', 2008, 'Vince Gilligan', 47, 5, 62)
        catalogue.add(series2)
        
        print(f"\n{catalogue}")
    except ValueError as e:
        print(f'Validation Error: {e}')
    except MediaError as e:
        print(f'Media Error: {e}')
        print(f'Unable to add {e.obj}: {type(e.obj)}')