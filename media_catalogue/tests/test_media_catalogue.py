import pytest
from media_catalogue import Movie, TVSeries, MediaCatalogue, MediaError


class TestMovie:
    """Tests for the Movie class."""

    # ==================== Happy Path Tests ====================

    def test_create_valid_movie(self):
        """Test creating a movie with valid inputs."""
        movie = Movie('The Matrix', 1999, 'The Wachowskis', 136)

        assert movie.title == 'The Matrix'
        assert movie.year == 1999
        assert movie.director == 'The Wachowskis'
        assert movie.duration == 136

    def test_movie_str_representation(self):
        """Test the string representation of a movie."""
        movie = Movie('The Matrix', 1999, 'The Wachowskis', 136)

        assert str(movie) == 'The Matrix (1999) - 136 min, The Wachowskis'

    # ==================== Boundary Tests ====================

    @pytest.mark.parametrize("title,year,director,duration", [
        pytest.param('First Film', 1895, 'Lumiere', 1, id='year_1895_first_valid'),
        pytest.param('Short', 2000, 'Director', 1, id='duration_1_minimum'),
        pytest.param('Future', 2099, 'Director', 120, id='year_2099_future'),
        pytest.param('A' * 500, 2000, 'Director', 90, id='very_long_title'),
        pytest.param('1917', 2019, 'Sam Mendes', 119, id='numeric_title_1917'),
        pytest.param('300', 2006, 'Zack Snyder', 117, id='numeric_title_300'),
        pytest.param('42', 2013, 'Brian Helgeland', 128, id='numeric_title_42'),
    ])
    def test_valid_movie_boundary_cases(self, title, year, director, duration):
        """Test that boundary values create valid movies."""
        movie = Movie(title, year, director, duration)

        assert movie.title == title
        assert movie.year == year

    # ==================== Validation Error Tests ====================

    @pytest.mark.parametrize("title,year,director,duration,expected_error", [
        pytest.param('', 2000, 'Director', 90, 'Title cannot be empty', id='empty_title'),
        pytest.param('   ', 2000, 'Director', 90, 'Title cannot be empty', id='whitespace_title'),
        pytest.param('Movie', 1800, 'Director', 90, 'Year must be 1895 or later', id='year_1800_too_early'),
        pytest.param('Movie', 1894, 'Director', 90, 'Year must be 1895 or later', id='year_1894_off_by_one'),
        pytest.param('Movie', 2000, '', 90, 'Director cannot be empty', id='empty_director'),
        pytest.param('Movie', 2000, '   ', 90, 'Director cannot be empty', id='whitespace_director'),
        pytest.param('Movie', 2000, '123', 90, 'Director must contain at least one letter', id='director_only_numbers'),
        pytest.param('Movie', 2000, '42', 90, 'Director must contain at least one letter', id='director_just_number'),
        pytest.param('Movie', 2000, 'Director', 0, 'Duration must be positive', id='zero_duration'),
        pytest.param('Movie', 2000, 'Director', -90, 'Duration must be positive', id='negative_duration'),
    ])
    def test_movie_validation_errors(self, title, year, director, duration, expected_error):
        """Test that invalid inputs raise appropriate ValueError."""
        with pytest.raises(ValueError) as e:
            Movie(title, year, director, duration)

        assert str(e.value) == expected_error

    # ==================== Type Validation Tests ====================

    @pytest.mark.parametrize("title,expected_error", [
        pytest.param(123, 'Title must be a string', id='title_int'),
        pytest.param(['The', 'Matrix'], 'Title must be a string', id='title_list'),
        pytest.param({'name': 'Movie'}, 'Title must be a string', id='title_dict'),
        pytest.param(None, 'Title must be a string', id='title_none'),
    ])
    def test_movie_title_type_validation(self, title, expected_error):
        """Test that non-string titles raise ValueError."""
        with pytest.raises(ValueError) as e:
            Movie(title, 2000, 'Director', 90)

        assert str(e.value) == expected_error

    @pytest.mark.parametrize("director,expected_error", [
        pytest.param(123, 'Director must be a string', id='director_int'),
        pytest.param(['John', 'Doe'], 'Director must be a string', id='director_list'),
        pytest.param({'name': 'Director'}, 'Director must be a string', id='director_dict'),
        pytest.param(None, 'Director must be a string', id='director_none'),
    ])
    def test_movie_director_type_validation(self, director, expected_error):
        """Test that non-string directors raise ValueError."""
        with pytest.raises(ValueError) as e:
            Movie('Movie', 2000, director, 90)

        assert str(e.value) == expected_error


class TestTVSeries:
    """Tests for the TVSeries class."""

    # ==================== Happy Path Tests ====================

    def test_create_valid_series(self):
        """Test creating a TV series with valid inputs."""
        series = TVSeries('Breaking Bad', 2008, 'Vince Gilligan', 47, 5, 62)

        assert series.title == 'Breaking Bad'
        assert series.year == 2008
        assert series.director == 'Vince Gilligan'
        assert series.duration == 47
        assert series.seasons == 5
        assert series.total_episodes == 62

    def test_series_str_representation(self):
        """Test the string representation of a TV series."""
        series = TVSeries('Breaking Bad', 2008, 'Vince Gilligan', 47, 5, 62)

        assert str(series) == 'Breaking Bad (2008) - 5 seasons, 62 episodes, 47 min avg, Vince Gilligan'

    # ==================== Boundary Tests ====================

    @pytest.mark.parametrize("seasons,episodes", [
        pytest.param(1, 1, id='minimum_1_season_1_episode'),
        pytest.param(1, 100, id='single_season_many_episodes'),
        pytest.param(50, 1, id='many_seasons_single_episode'),
    ])
    def test_valid_series_boundary_cases(self, seasons, episodes):
        """Test that boundary values create valid series."""
        series = TVSeries('Test Show', 2020, 'Director', 30, seasons, episodes)

        assert series.seasons == seasons
        assert series.total_episodes == episodes

    # ==================== Validation Error Tests ====================

    @pytest.mark.parametrize("seasons,episodes,expected_error", [
        pytest.param(0, 10, 'Seasons must be 1 or greater', id='zero_seasons'),
        pytest.param(-1, 10, 'Seasons must be 1 or greater', id='negative_seasons'),
        pytest.param(-5, 10, 'Seasons must be 1 or greater', id='very_negative_seasons'),
        pytest.param(1, 0, 'Total episodes must be 1 or greater', id='zero_episodes'),
        pytest.param(1, -1, 'Total episodes must be 1 or greater', id='negative_episodes'),
        pytest.param(1, -100, 'Total episodes must be 1 or greater', id='very_negative_episodes'),
    ])
    def test_series_validation_errors(self, seasons, episodes, expected_error):
        """Test that invalid seasons/episodes raise appropriate ValueError."""
        with pytest.raises(ValueError) as e:
            TVSeries('Test Show', 2020, 'Director', 30, seasons, episodes)

        assert str(e.value) == expected_error

    def test_series_inherits_movie_validation(self):
        """Test that TVSeries inherits validation from Movie."""
        with pytest.raises(ValueError) as e:
            TVSeries('', 2020, 'Director', 30, 1, 10)

        assert str(e.value) == 'Title cannot be empty'


class TestMediaCatalogue:
    """Tests for the MediaCatalogue class."""

    # ==================== Happy Path Tests ====================

    def test_empty_catalogue_str(self):
        """Test string representation of empty catalogue."""
        catalogue = MediaCatalogue()

        assert str(catalogue) == 'Media Catalogue (empty)'

    def test_empty_catalogue_length(self):
        """Test that empty catalogue has zero items."""
        catalogue = MediaCatalogue()

        assert len(catalogue.items) == 0

    def test_add_movie_to_catalogue(self):
        """Test adding a movie to the catalogue."""
        catalogue = MediaCatalogue()
        movie = Movie('Inception', 2010, 'Christopher Nolan', 148)
        catalogue.add(movie)

        assert len(catalogue.items) == 1
        assert catalogue.items[0] == movie

    def test_add_series_to_catalogue(self):
        """Test adding a TV series to the catalogue."""
        catalogue = MediaCatalogue()
        series = TVSeries('Scrubs', 2001, 'Bill Lawrence', 24, 9, 182)
        catalogue.add(series)

        assert len(catalogue.items) == 1
        assert catalogue.items[0] == series

    def test_add_multiple_items(self):
        """Test adding multiple items to catalogue."""
        catalogue = MediaCatalogue()
        movie = Movie('Inception', 2010, 'Christopher Nolan', 148)
        series = TVSeries('Breaking Bad', 2008, 'Vince Gilligan', 47, 5, 62)

        catalogue.add(movie)
        catalogue.add(series)

        assert len(catalogue.items) == 2

    def test_catalogue_str_with_items(self):
        """Test string representation with items."""
        catalogue = MediaCatalogue()
        movie = Movie('Inception', 2010, 'Christopher Nolan', 148)
        catalogue.add(movie)

        result = str(catalogue)
        assert 'Media Catalogue (1 items)' in result
        assert 'Inception' in result

    # ==================== Invalid Item Tests ====================

    @pytest.mark.parametrize("invalid_item,item_type", [
        pytest.param("not a movie", str, id='string'),
        pytest.param(42, int, id='integer'),
        pytest.param(3.14, float, id='float'),
        pytest.param(None, type(None), id='none'),
        pytest.param(['a', 'list'], list, id='list'),
        pytest.param({'title': 'Fake'}, dict, id='dict'),
    ])
    def test_catalogue_rejects_invalid_types(self, invalid_item, item_type):
        """Test that adding non-Movie/TVSeries raises MediaError."""
        catalogue = MediaCatalogue()

        with pytest.raises(MediaError) as e:
            catalogue.add(invalid_item)

        assert str(e.value) == 'Only Movie or TVSeries instances can be added'
        assert e.value.obj == invalid_item
        assert isinstance(e.value.obj, item_type)

    # ==================== Delete Tests ====================

    def test_delete_movie_from_catalogue(self):
        """Test deleting a movie from the catalogue."""
        catalogue = MediaCatalogue()
        movie = Movie('Inception', 2010, 'Christopher Nolan', 148)
        catalogue.add(movie)

        deleted = catalogue.delete(movie)

        assert len(catalogue.items) == 0
        assert deleted == movie

    def test_delete_series_from_catalogue(self):
        """Test deleting a TV series from the catalogue."""
        catalogue = MediaCatalogue()
        series = TVSeries('Breaking Bad', 2008, 'Vince Gilligan', 47, 5, 62)
        catalogue.add(series)

        deleted = catalogue.delete(series)

        assert len(catalogue.items) == 0
        assert deleted == series

    def test_delete_returns_deleted_item(self):
        """Test that delete returns the deleted item."""
        catalogue = MediaCatalogue()
        movie = Movie('The Matrix', 1999, 'The Wachowskis', 136)
        catalogue.add(movie)

        result = catalogue.delete(movie)

        assert result is movie
        assert result.title == 'The Matrix'

    def test_delete_nonexistent_item_raises_error(self):
        """Test that deleting a non-existent item raises MediaError."""
        catalogue = MediaCatalogue()
        movie = Movie('Inception', 2010, 'Christopher Nolan', 148)

        with pytest.raises(MediaError) as e:
            catalogue.delete(movie)

        assert str(e.value) == 'Item not found in catalogue'
        assert e.value.obj == movie

    def test_delete_from_multiple_items(self):
        """Test deleting one item from a catalogue with multiple items."""
        catalogue = MediaCatalogue()
        movie1 = Movie('Inception', 2010, 'Christopher Nolan', 148)
        movie2 = Movie('The Matrix', 1999, 'The Wachowskis', 136)
        catalogue.add(movie1)
        catalogue.add(movie2)

        catalogue.delete(movie1)

        assert len(catalogue.items) == 1
        assert catalogue.items[0] == movie2

    # ==================== Get Movies / Get TV Series Tests ====================

    def test_get_movies_returns_only_movies(self):
        """Test that get_movies returns only Movie instances, not TVSeries."""
        catalogue = MediaCatalogue()
        movie = Movie('Inception', 2010, 'Christopher Nolan', 148)
        series = TVSeries('Breaking Bad', 2008, 'Vince Gilligan', 47, 5, 62)
        catalogue.add(movie)
        catalogue.add(series)

        movies = catalogue.get_movies()

        assert len(movies) == 1
        assert movies[0] == movie
        assert type(movies[0]) is Movie

    def test_get_tv_series_returns_only_series(self):
        """Test that get_tv_series returns only TVSeries instances."""
        catalogue = MediaCatalogue()
        movie = Movie('Inception', 2010, 'Christopher Nolan', 148)
        series = TVSeries('Breaking Bad', 2008, 'Vince Gilligan', 47, 5, 62)
        catalogue.add(movie)
        catalogue.add(series)

        tv_series = catalogue.get_tv_series()

        assert len(tv_series) == 1
        assert tv_series[0] == series
        assert type(tv_series[0]) is TVSeries

    def test_get_movies_empty_catalogue(self):
        """Test get_movies on empty catalogue returns empty list."""
        catalogue = MediaCatalogue()

        assert catalogue.get_movies() == []

    def test_get_tv_series_empty_catalogue(self):
        """Test get_tv_series on empty catalogue returns empty list."""
        catalogue = MediaCatalogue()

        assert catalogue.get_tv_series() == []

    @pytest.mark.parametrize("num_movies,num_series", [
        pytest.param(3, 0, id='only_movies'),
        pytest.param(0, 3, id='only_series'),
        pytest.param(2, 2, id='mixed_equal'),
        pytest.param(5, 1, id='more_movies'),
        pytest.param(1, 5, id='more_series'),
    ])
    def test_get_movies_and_series_counts(self, num_movies, num_series):
        """Test that get_movies and get_tv_series return correct counts."""
        catalogue = MediaCatalogue()

        for i in range(num_movies):
            catalogue.add(Movie(f'Movie {i}', 2000 + i, 'Director', 90))
        for i in range(num_series):
            catalogue.add(TVSeries(f'Series {i}', 2000 + i, 'Director', 45, 1, 10))

        assert len(catalogue.get_movies()) == num_movies
        assert len(catalogue.get_tv_series()) == num_series

    # ==================== Filter Tests ====================

    @pytest.mark.parametrize("filter_type,expected_count", [
        pytest.param('movie', 2, id='filter_movies'),
        pytest.param('series', 1, id='filter_series'),
    ])
    def test_filter_by_series_or_movie(self, filter_type, expected_count):
        """Test filter_by_series_or_movie returns correct items."""
        catalogue = MediaCatalogue()
        catalogue.add(Movie('Movie 1', 2000, 'Director', 90))
        catalogue.add(Movie('Movie 2', 2001, 'Director', 100))
        catalogue.add(TVSeries('Series 1', 2002, 'Director', 45, 1, 10))

        result = catalogue.filter_by_series_or_movie(filter_type)

        assert len(result) == expected_count

    @pytest.mark.parametrize("invalid_type", [
        pytest.param('movies', id='typo_movies'),
        pytest.param('tv', id='wrong_tv'),
        pytest.param('', id='empty_string'),
        pytest.param('MOVIE', id='uppercase'),
    ])
    def test_filter_invalid_type_raises_error(self, invalid_type):
        """Test that invalid filter types raise ValueError."""
        catalogue = MediaCatalogue()

        with pytest.raises(ValueError) as e:
            catalogue.filter_by_series_or_movie(invalid_type)

        assert str(e.value) == 'Invalid type. Must be "movie" or "series"'
