from datetime import datetime
from random import randint

AMOUNT_OF_DAYS = 11
DEVIATION_PERCENTAGE = 10
NAMES_FILE = "./CSV_Database_of_First_Names.csv"
SECONDS_IN_MINUTE = 60
MINUTES_IN_HOUR = 60
HOUR_SHEET = [
    # night
    5, 5, 5, 5, 5, 5,

    # morning
    5, 5, 10, 100, 80, 50,

    # afternoon
    30, 30, 30, 30, 30, 20,

    # evening
    10, 10, 10, 10, 10, 10
]


def rand_name(names):
    """
    Gets a random name from the list of names
    :param names:  The list of names.
    :return: A random name from the list.
    """
    return names[randint(0, len(names) - 1)]


def load_names():
    """
    Loads names from a file.
    :return: A list containing the names.
    """
    temp_names = []

    with open(NAMES_FILE) as f:
        for line in f:
            if len(line.strip()) > 0:
                temp_names.append(line.strip())

    return temp_names


def random_between_bounds(number):
    """
    Generates a random number with a random deviation.
    :param number: The number to deviate around.
    :return: A random number.
    """
    min_bound = round(number - number / (100 / DEVIATION_PERCENTAGE))
    max_bound = round(number + number / (100 / DEVIATION_PERCENTAGE))

    return randint(min_bound, max_bound)


def generate_datetime(hour):
    """
    Generates a datetime with random minutes and seconds.
    :param hour: The hour of the datetime.
    :return: A datetime with random minutes and seconds.
    """
    minute = randint(0, MINUTES_IN_HOUR - 1)
    second = randint(0, SECONDS_IN_MINUTE - 1)

    return datetime.strptime(str(hour) + ":"
                             + str(minute) + ":"
                             + str(second), '%H:%M:%S')


def generate_day_cycle(names):
    """
    Generates one day cycle of logs.
    :param names: A list of names to be randomly added to the logs.
    :return: A log of a single day cycle in a list.
    """
    day_log = []

    for i in range(0, len(HOUR_SHEET)):

        for time in range(0, random_between_bounds(HOUR_SHEET[i])):
            log_time = generate_datetime(i)

            day_log.append([log_time, rand_name(names), 1])

    day_log.sort()

    return day_log


def generate_days(nr_of_days):
    """
    Generates multiple day cycles.
    :param nr_of_days: Number of day cycles to generate.
    :return: A log containing multiple day cycles.
    """
    log = []
    names = load_names()

    for i in range(0, nr_of_days):
        day_log = generate_day_cycle(names)

        for entry in day_log:
            log.append(entry)

    return log


# Code to run:
log = generate_days(365)

for x in log:
    print(str(x[0].time()) + ", " + x[1] + ", " + str(x[2]))

print("Random name: " + rand_name(load_names()))
