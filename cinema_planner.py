import click
from cinemaPlanner.planner import get_screenings_combinations_from_csv


@click.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--time-between-screenings', default=15, help='Time in minutes between screenings')
@click.option('--max-movies', default=3, help='Maximum number of movies to watch in one day')
def plan_cinema(path, max_movies, time_between_screenings):
    """Plan cinema screenings from a CSV file located in PATH"""
    combinations = get_screenings_combinations_from_csv(path, max_movies, time_between_screenings)
    for combination in combinations:
        print(combination)


if __name__ == "__main__":
    plan_cinema()
