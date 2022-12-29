"""
Given a list of one cinema screening, the planner should only return this screening.

Given a list of two cinema screenings of two different movies, if they don't intersect, the planner should return both screenings in one result.
Given a list of two cinema screenings of two different movies, if they intersect, the planner should return no result.
Given a list of two cinema screening of the same movie, if they don't intersect, the planner should return no result.
Given a list of multiple cinema screenings of two movies, in each result, the planner should return one possible combination of screenings that don't intersect.
"""

import pytest
from planner import CinemaScreening, get_screenings_combinations, read_cinema_screenings_from_csv

def test_one_screening():
    screenings = [CinemaScreening("The Matrix", "12:00", 120)]
    assert get_screenings_combinations(screenings) == [[screenings[0]]]

def test_two_screenings_of_different_movies_that_dont_intersect():
    screenings = [
        CinemaScreening("The Matrix", "12:00", 120),
        CinemaScreening("The Matrix Reloaded", "14:00", 120),
    ]
    assert get_screenings_combinations(screenings) == [[screenings[0], screenings[1]]]

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
    assert get_screenings_combinations(screenings) == [
        [screenings[0], screenings[1], screenings[2]],
        [screenings[1], screenings[2]],
    ]

def test_multiple_screenings_of_three_movies():
    screenings = [
        CinemaScreening("The Matrix", "12:00", 120),
        CinemaScreening("The Matrix Reloaded", "14:00", 120),
        CinemaScreening("The Matrix Revolutions", "16:00", 120),
        CinemaScreening("The Matrix 4", "18:00", 120),
    ]
    assert get_screenings_combinations(screenings) == [
        [screenings[0], screenings[1], screenings[2], screenings[3]],
        [screenings[0], screenings[2], screenings[3]],
        [screenings[1], screenings[2], screenings[3]],
        [screenings[2], screenings[3]],
    ]

def csv_test_two_movies():
    screenings = read_cinema_screenings_from_csv("test/resources/screenings_two_movies.csv")
    combinations = get_screenings_combinations(screenings)
    assert combinations != []
    assert [screenings[2], screenings[6]] in combinations
    for combination in combinations:
        assert len(combination) == 2
        assert combination[0].movie != combination[1].movie
        assert not combination[0].get_ending_time_in_minutes() > combination[1].start_time_in_minutes


def csv_test_three_movies():
    screenings = read_cinema_screenings_from_csv("test/resources/screenings_three_movies.csv")
    combinations = get_screenings_combinations(screenings)
    assert combinations != []
    for combination in combinations:
        assert len(combination) >= 2
        assert combination[0].movie != combination[1].movie != combination[2].movie
        assert combination[0].get_ending_time_in_minutes() <= combination[1].start_time_in_minutes \
               and combination[1].get_ending_time_in_minutes() <= combination[2].start_time_in_minutes