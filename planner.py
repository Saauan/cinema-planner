"""The planner module should be able to take a list of screenings and return a list of combinations of screenings of
different movies that don't intersect in time."""
from typing import List


class CinemaScreening:
    """
    The cinema screening class has the following attributes

    Attributes:
        - movie (str) : the movie being screened
        - start_time (int|str) : the start time of the screening in minutes or in the format "HH:MM".
            If it's an int, it's the number of minutes since midnight.
            If it's a str, it's in the format "HH:MM" where HH is the number of hours since midnight
            and MM is the number of minutes since the last hour and is then internally converted in minutes.
        - duration (int) : the duration of the screening in minutes
    """

    def __init__(self, movie: str, start_time: int | str, duration: int):
        self.movie = movie
        self.start_time_in_minutes = convert_start_time_in_minutes(start_time)
        self.duration = duration

    def get_start_time_in_human_readable_format(self):
        return convert_time_in_minutes_to_human_readable(self.start_time_in_minutes)

    def get_ending_time_in_minutes(self):
        return self.start_time_in_minutes + self.duration

    def __repr__(self):
        return f"{self.movie} ({self.get_start_time_in_human_readable_format()} - {convert_time_in_minutes_to_human_readable(self.get_ending_time_in_minutes())})"

    def __eq__(self, other):
        return self.movie == other.movie and self.start_time_in_minutes == other.start_time_in_minutes and self.duration == other.duration

def get_screenings_combinations(screenings: List[CinemaScreening]) -> List[List[CinemaScreening]]:
    """
    Return a list of all the possible combinations of screenings of different movies that don't intersect.

    Each result must have more than one screening.

    Examples :
    >>> get_screenings_combinations([CinemaScreening("movie1", 0, 60), CinemaScreening("movie2", 60, 60)])
    [[movie1 (00:00 - 01:00)], [movie2 (01:00 - 02:00)]]
    >>> get_screenings_combinations([CinemaScreening("movie1", 0, 60), CinemaScreening("movie2", 60, 60), CinemaScreening("movie3", 120, 60)])
    [[movie1 (00:00 - 01:00)], [movie2 (01:00 - 02:00)], [movie3 (02:00 - 03:00)], [movie1 (00:00 - 01:00), movie2 (01:00 - 02:00)], [movie1 (00:00 - 01:00), movie3 (02:00 - 03:00)], [movie2 (01:00 - 02:00), movie3 (02:00 - 03:00)]]
    >>> get_screenings_combinations([CinemaScreening("movie1", 0, 60), CinemaScreening("movie2", 60, 60)], CinemaScreening("movie2", 30, 60)], CinemaScreening("movie2", 120, 60)])
    [[movie1 (00:00 - 01:00)], [movie2 (01:00 - 02:00)], [movie1 (00:00 - 01:00), movie2 (02:00 - 03:00)]]
    """
    # Sorts the list of screening by start time
    screenings.sort(key=lambda screening: screening.start_time_in_minutes)

    if len(screenings) == 1:
        return [screenings]
    combinations = []
    # Separate the screenings into lists by movie
    screenings_by_movie = {}
    for screening in screenings:
        if screening.movie not in screenings_by_movie:
            screenings_by_movie[screening.movie] = []
        screenings_by_movie[screening.movie].append(screening)
    # We choose a starting movie. So for every movie
    for movie, movie_screenings in screenings_by_movie.items():
        # For every screening of the movie
        for current_screening in movie_screenings:
            current_combinations = []
            for other_movie, other_movie_screenings in screenings_by_movie.items():
                # If the movie is not the starting movie
                if other_movie != movie:
                    # Find the first screening of the other movie that doesn't intersect with the starting screening
                    first_available_screening = find_first_available_screening(other_movie_screenings, current_screening)
                    if first_available_screening is not None:
                        current_combinations.append([current_screening, first_available_screening])
            # If there are more than two movies
            if len(screenings_by_movie) > 2:
                # We do another loop to find the first available screening for the second screening of the combination
                new_combinations = []
                for combination in current_combinations:
                    for other_movie, other_movie_screenings in screenings_by_movie.items():
                        # If the movie is not in the combination
                        if other_movie != combination[0].movie and other_movie != combination[1].movie:
                            # Find the first screening of the other movie that doesn't intersect with the last screening in the combination
                            first_available_screening = find_first_available_screening(other_movie_screenings, combination[1])
                            if first_available_screening is not None:
                                new_combinations.append([combination[0], combination[1], first_available_screening])
                            else:
                                new_combinations.append(combination)
                combinations += new_combinations
            else:
                combinations += current_combinations

    return combinations


def find_first_available_screening(other_movie_screenings, screening):
    for other_screening in other_movie_screenings:
        if not does_screening_intersect(screening, other_screening):
            # If the combination of the two screenings doesn't intersect with any other screenings
            if not does_screening_intersect(screening, other_screening):
                # Add the combination to the list of combinations
                return other_screening
    return None


def read_cinema_screenings_from_csv(file_path):
    screenings = []
    with open(file_path) as csv_file:
        # skip header line
        next(csv_file)
        for line in csv_file:
            movie, start_time, duration = line.strip().split(",")
            screenings.append(CinemaScreening(movie, start_time, int(duration)))
    return screenings

def get_screenings_combinations_from_csv(file_path):
    return get_screenings_combinations(read_cinema_screenings_from_csv(file_path))

def does_combination_intersect(combination: List[CinemaScreening], screening: CinemaScreening) -> bool:
    """
    Return True if the combination of screenings intersects with the screening or if one screening in the combination
    is the same movie as the screening.
    """
    for other_screening in combination:
        if does_screening_intersect(other_screening, screening) or other_screening.movie == screening.movie:
            return True
    return False


def does_screening_intersect(screening1: CinemaScreening, screening2: CinemaScreening):
    """
    Two movies intersect if the second starts before the first ends.
    :param screening1:
    :param screening2:
    :return:
    """
    return screening2.start_time_in_minutes < screening1.get_ending_time_in_minutes()

def convert_start_time_in_minutes(start_time):
    if isinstance(start_time, str):
        hours, minutes = start_time.split(":")
        return int(hours) * 60 + int(minutes)
    return start_time


def convert_time_in_minutes_to_human_readable(minutes):
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours:02d}:{minutes:02d}"
