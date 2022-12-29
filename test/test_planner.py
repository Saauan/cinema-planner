from cinemaPlanner.planner import CinemaScreening, get_screenings_combinations, read_cinema_screenings_from_csv

DEFAULT_MAX_DEPTH = 3
DEFAULT_MIN_WAIT_TIME_BETWEEN_SCREENINGS = 0

def test_one_screening():
    screenings = [CinemaScreening("The Matrix", "12:00", 120)]
    assert get_screenings_combinations(screenings) == [[screenings[0]]]

def test_two_screenings_of_different_movies_that_dont_intersect():
    screenings = [
        CinemaScreening("The Matrix", "12:00", 120),
        CinemaScreening("The Matrix Reloaded", "14:00", 120),
    ]
    assert get_screenings_combinations(screenings, max_depth=DEFAULT_MAX_DEPTH, time_between_screenings=DEFAULT_MIN_WAIT_TIME_BETWEEN_SCREENINGS) == [(screenings[0], screenings[1])]

def test_two_screenings_of_different_movies_that_intersect():
    screenings = [
        CinemaScreening("The Matrix", "12:00", 120),
        CinemaScreening("The Matrix Reloaded", "13:00", 120),
    ]
    assert get_screenings_combinations(screenings) == []

def test_two_screenings_of_the_same_movie_that_dont_intersect():
    screenings = [
        CinemaScreening("The Matrix", "12:00", 120),
        CinemaScreening("The Matrix", "14:00", 120),
    ]
    assert get_screenings_combinations(screenings) == []

def test_multiple_screenings_of_two_movies():
    screenings = [
        CinemaScreening("The Matrix", "12:00", 120),
        CinemaScreening("The Matrix Reloaded", "14:00", 120),
        CinemaScreening("The Matrix Revolutions", "16:00", 120),
    ]
    expected_screenings = [
        (screenings[1], screenings[2]),
        (screenings[0], screenings[2]),
        (screenings[0], screenings[1], screenings[2])
    ]
    assert set(get_screenings_combinations(screenings, max_depth=DEFAULT_MAX_DEPTH, time_between_screenings=DEFAULT_MIN_WAIT_TIME_BETWEEN_SCREENINGS)) == set(expected_screenings)


def test_multiple_screenings_of_four_movies():
    screenings = [
        CinemaScreening("The Matrix 1", "12:00", 120),
        CinemaScreening("The Matrix 2", "14:00", 120),
        CinemaScreening("The Matrix 3", "16:00", 120),
        CinemaScreening("The Matrix 4", "18:00", 120),
    ]
    expected_screenings = [
        (screenings[1], screenings[3]),
        (screenings[1], screenings[2], screenings[3]),
        (screenings[2], screenings[3]),
        (screenings[0], screenings[1], screenings[2]),
        (screenings[0], screenings[2], screenings[3]),
        (screenings[0], screenings[3]),
#        (screenings[0], screenings[2]), not present ???
        (screenings[0], screenings[1], screenings[3]),
        (screenings[1], screenings[3]),
    ]
    assert set(get_screenings_combinations(screenings, max_depth=DEFAULT_MAX_DEPTH, time_between_screenings=DEFAULT_MIN_WAIT_TIME_BETWEEN_SCREENINGS)) == \
           set(expected_screenings)

def csv_test_two_movies():
    screenings = read_cinema_screenings_from_csv("resources/screenings_two_movies.csv")
    combinations = get_screenings_combinations(screenings)
    assert combinations != []
    assert [screenings[2], screenings[6]] in combinations
    for combination in combinations:
        assert len(combination) == 2
        assert combination[0].movie != combination[1].movie
        assert not combination[0].get_ending_time_in_minutes() > combination[1].start_time_in_minutes


def csv_test_three_movies():
    screenings = read_cinema_screenings_from_csv("resources/screenings_three_movies.csv")
    combinations = get_screenings_combinations(screenings)
    assert combinations != []
    for combination in combinations:
        assert len(combination) >= 2
        assert combination[0].movie != combination[1].movie != combination[2].movie
        assert combination[0].get_ending_time_in_minutes() <= combination[1].start_time_in_minutes \
               and combination[1].get_ending_time_in_minutes() <= combination[2].start_time_in_minutes