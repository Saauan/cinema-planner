"""The planner module should be able to take a list of screenings and return a list of combinations of screenings of
different movies that don't intersect in time."""
from typing import List

MAX_MOVIES = 3
MIN_WAIT_TIME_BETWEEN_SCREENINGS = 60


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

    def __hash__(self):
        return hash((self.movie, self.start_time_in_minutes, self.duration))

def get_screenings_combinations(screenings: List[CinemaScreening], max_depth = MAX_MOVIES, time_between_screenings = MIN_WAIT_TIME_BETWEEN_SCREENINGS) -> List[List[CinemaScreening]]:
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
    # Separate the screenings into lists by movie
    screenings_by_movie = {}
    for screening in screenings:
        if screening.movie not in screenings_by_movie:
            screenings_by_movie[screening.movie] = []
        screenings_by_movie[screening.movie].append(screening)
    # As long as we can add a screening to the combinations
    combinations = []
    for screening in screenings:
        combinations.append((screening,))
    depth = 1
    while depth < max_depth:
        new_combinations = set()
        for combination in combinations:
            anything_added = False
            for other_movie, other_movie_screenings in screenings_by_movie.items():
                if other_movie not in [screening.movie for screening in combination]:
                    first_available_screening = find_first_available_screening(other_movie_screenings, combination[-1], time_between_screenings)
                    if first_available_screening:
                        new_combinations.add(combination + (first_available_screening,))
                        anything_added = True
            if not anything_added:
                new_combinations.add(combination)
        combinations = list(new_combinations)
        depth+= 1
    # Order the combinations list by movie name and start time
    combinations.sort(key=lambda combination: combination[0].movie + str(combination[0].get_start_time_in_human_readable_format()))
    # Filter combinations with only one screening
    filtered_combinations = [combination for combination in combinations if len(combination) > 1]
    return filtered_combinations

def find_first_available_screening(other_movie_screenings, screening, time_between_screenings):
    for other_screening in other_movie_screenings:
        if not does_screening_intersect(screening, other_screening, time_between_screenings):
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


def does_screening_intersect(screening1: CinemaScreening, screening2: CinemaScreening,
                             time_between_screenings):
    """
    Two movies intersect if the second starts before the first ends.
    :param screening1:
    :param screening2:
    :return:
    """
    return screening2.start_time_in_minutes < screening1.get_ending_time_in_minutes() + time_between_screenings

def convert_start_time_in_minutes(start_time):
    if isinstance(start_time, str):
        hours, minutes = start_time.split(":")
        return int(hours) * 60 + int(minutes)
    return start_time


def convert_time_in_minutes_to_human_readable(minutes):
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours:02d}:{minutes:02d}"
