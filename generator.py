from datetime import datetime
from datetime import timedelta
from random import randint

log = [[]]

begin_time = datetime.strptime("00:00:00", '%H:%M:%S')
amount_of_hours = 11
range_percentage = 10;
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

            day_log.append([log_time, "usr", 1])

    day_log.sort()

    return day_log


log = generate_day_cycle()

for x in log:
    print(x[0].time())
