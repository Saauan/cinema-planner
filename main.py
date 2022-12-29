from planner import get_screenings_combinations_from_csv

if __name__ == "__main__":
    combinations = get_screenings_combinations_from_csv("resources/screenings.csv")
    for combination in combinations:
        print(combination)