import os.path
from datetime import datetime
from datetime import timedelta
from random import randint

AMOUNT_OF_DAYS = 11
DEVIATION_PERCENTAGE = 10
NAMES_FILE = "./CSV_Database_of_First_Names.csv"
GENERATE_FILE = "./generated-log.csv"
SECONDS_IN_MINUTE = 60
SECONDS_IN_DAY = 86400
MINUTES_IN_HOUR = 60
MAX_NR_OF_ATTACKS = 100000
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
BRUTEFORCE_CHANCE_SHEET = [
    # night
    1000, 1000, 1000, 1000, 1000, 1000,

    # morning
    1000, 1000, 9000, 10000, 10000, 5000,

    # afternoon
    30000, 30000, 30000, 30000, 30000, 20000,

    # evening
    1000, 1000, 1000, 1000, 1000, 1000
]


def random_with_deviation(number):
    """
    Generates a random number with a random deviation.
    
    :param number: The number to deviate around.
    :return: A random number.
    """
    min_bound = round(number - number / (100 / DEVIATION_PERCENTAGE))
    max_bound = round(number + number / (100 / DEVIATION_PERCENTAGE))

    return randint(min_bound, max_bound)


def is_time_for_bruteforce(hour):
    """
    Randomly determines if it's time for bruteforce. This depends on the hour of day.
    Change per hour of day is determined in BRUTEFORCE_CHANCE_SHEET.
    
    :param hour: The hour of the day.
    :return: A boolean representing whether or not it's time for bruteforce.
    """
    number_to_guess = randint(0, BRUTEFORCE_CHANCE_SHEET[hour])
    guess = randint(0, BRUTEFORCE_CHANCE_SHEET[hour])

    return number_to_guess == guess


def generate_brutforce_log(hour, names):
    """
    Generates a bruteforce log which begins somewhere in a given hour and ends 
    when a random amount of attacks have been logged.
    
    :param hour: The hour in which the attacks begin.
    :param names: A list of names.
    :return: A list containing the log of the attack.
    """
    time = generate_datetime(hour)
    d = timedelta(seconds=1)
    attacks_per_second = \
        random_with_deviation(MAX_NR_OF_ATTACKS / SECONDS_IN_DAY)
    username = rand_name(names)
    duration = randint(0, SECONDS_IN_DAY - 1)
    log = []
    count = 0

    while count < duration:
        for i in range(0, attacks_per_second):
            log.append([time, username, 0, 0])

        count += 1
        time += d

    return log


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
        if is_time_for_bruteforce(i):
            b_log = generate_brutforce_log(i, names)

            for entry in b_log:
                day_log.append(entry)

        for time in range(0, random_with_deviation(HOUR_SHEET[i])):
            log_time = generate_datetime(i)

            day_log.append([log_time, rand_name(names), 1, 1])

    day_log.sort()

    return day_log


def export_to_csv(log):
    """
    Generates a CSV file of the log list.
    
    :param log: The log list.
    """
    if os.path.isfile(GENERATE_FILE):
        os.remove(GENERATE_FILE)

    with open(GENERATE_FILE, "w") as f:
        f.write("time, username, succes, label\n")

        for entry in log:
            f.write(str(entry[0].time()) + ", "
                    + str(entry[1]) + ", "
                    + str(entry[2]) + ", "
                    + str(entry[3])
                    + "\n")


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

export_to_csv(log)
