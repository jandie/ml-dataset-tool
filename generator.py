from datetime import datetime
from random import randint

begin_time = datetime.strptime("00:00:00", '%H:%M:%S')
amount_of_hours = 11
range_percentage = 10
logins_per_hour = [
    # night
    5, 5, 5, 5, 5, 5,

    # morning
    5, 5, 10, 100, 80, 50,

    # afternoon
    30, 30, 30, 30, 30, 20,

    # evening
    10, 10, 10, 10, 10, 10
]


def rand_name(list_of_names):
    max = len(list_of_names)

    return list_of_names[randint(0, max - 1)]


def load_names():
    temp_names = []

    with open("./CSV_Database_of_First_Names.csv") as f:
        for line in f:
            if len(line.strip()) > 0:
                temp_names.append(line.strip())

    return temp_names


names = load_names()


def random_between_bounds(lph):
    min_bound = round(lph - lph / (100 / range_percentage))
    max_bound = round(lph + lph / (100 / range_percentage))

    return randint(min_bound, max_bound)


def generate_datetime(hour):
    minute = randint(0, 59)
    second = randint(0, 59)

    return datetime.strptime(str(hour) + ":"
                             + str(minute) + ":"
                             + str(second), '%H:%M:%S')


def generate_day_cycle():
    day_log = []

    for i in range(0, len(logins_per_hour)):

        for time in range(0, random_between_bounds(logins_per_hour[i])):
            log_time = generate_datetime(i)

            day_log.append([log_time, rand_name(names), 1])

    day_log.sort()

    return day_log


def generate_days(number_of_names):
    temp_log = []

    for i in range(0, number_of_names):
        temp_day_log = generate_day_cycle()

        for entry in temp_day_log:
            temp_log.append(entry)

    return temp_log


log = generate_days(1000)

for x in log:
    print(str(x[0].time()) + ", " + x[1] + ", " + str(x[2]))

print("Random name: " + rand_name(names))
