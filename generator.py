import os.path
import sys
from datetime import datetime
from datetime import timedelta
from random import randint


class Generator:
    DEVIATION_PERCENTAGE = 10
    NAMES_FILE = "./CSV_Database_of_First_Names.csv"
    GENERATE_FILE = "./generated-log.csv"
    SECONDS_IN_MINUTE = 60
    SECONDS_IN_DAY = 86400
    MINUTES_IN_HOUR = 60
    MAX_NR_OF_ATTACKS = 50000
    BEGIN_DATE = datetime.strptime('2017-05-12', '%Y-%m-%d')
    CHANCE_TO_FUCK_UP = 3
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
    BRUTE_FORCE_CHANCE_SHEET = [
        # night
        1000, 1000, 1000, 1000, 1000, 1000,

        # morning
        1000, 1000, 9000, 10000, 10000, 5000,

        # afternoon
        30000, 30000, 30000, 30000, 30000, 20000,

        # evening
        1000, 1000, 1000, 1000, 1000, 1000
    ]



    def __init__(self):
        self.date = self.BEGIN_DATE

        # Check if Python version 3 is used
        if sys.version_info[0] != 3:
            raise EnvironmentError("Python 3 is required for this script to function properly")

    def random_with_deviation(self, number):
        """
        Generates a random number with a random deviation.
        
        :param number: The number to deviate around.
        :return: A random number.
        """
        min_bound = round(number - number / (100 / self.DEVIATION_PERCENTAGE))
        max_bound = round(number + number / (100 / self.DEVIATION_PERCENTAGE))

        return randint(min_bound, max_bound)

    def simulate_chance(self, chance):
        """
        Simulates a chance and randomly determines if the chance has occurred. 
        
        :param chance: The chance of this fucntion to return true.
        :return: A boolean representing whether or not the chance has occurred.
        """
        number_to_guess = randint(0, chance)
        guess = randint(0, chance)

        return number_to_guess == guess

    def is_time_for_bruteforce(self, hour):
        """
        Randomly determines if it's time for bruteforce. This depends on the hour of day.
        Change per hour of day is determined in BRUTEFORCE_CHANCE_SHEET.
        
        :param hour: The hour of the day.
        :return: A boolean representing whether or not it's time for bruteforce.
        """

        return self.simulate_chance(self.BRUTE_FORCE_CHANCE_SHEET[hour])

    def generate_brute_force_log(self, hour, names):
        """
        Generates a bruteforce log which begins somewhere in a given hour and ends 
        when a random amount of attacks have been logged.
        
        :param hour: The hour in which the attacks begin.
        :param names: A list of names.
        :return: A list containing the log of the attack.
        """
        time = self.generate_datetime(hour)
        d = timedelta(seconds=randint(1, 3))
        attacks_per_second = \
            self.random_with_deviation(self.MAX_NR_OF_ATTACKS / self.SECONDS_IN_DAY)
        username = self.rand_name(names)
        duration = randint(0, self.SECONDS_IN_DAY - 1)
        log = []
        count = 0

        while count < duration:
            for i in range(0, attacks_per_second):
                log.append([time, username, 0, 0])

            count += 1

            d = timedelta(seconds=randint(0, 3))
            time += d

        return log

    def rand_name(self, names):
        """
        Gets a random name from the list of names
        
        :param names:  The list of names.
        :return: A random name from the list.
        """
        return randint(0, len(names) - 1)

    def load_names(self):
        """
        Loads names from a file.
        
        :return: A list containing the names.
        """
        temp_names = []

        with open(self.NAMES_FILE) as f:
            for line in f:
                if len(line.strip()) > 0:
                    temp_names.append(line.strip())

        return temp_names

    def generate_datetime(self, hour):
        """
        Generates a datetime with random minutes and seconds.
        
        :param hour: The hour of the datetime.
        :return: A datetime with random minutes and seconds.
        """
        minute = randint(0, self.MINUTES_IN_HOUR - 1)
        second = randint(0, self.SECONDS_IN_MINUTE - 1)

        return datetime.strptime(str(self.date.year) + "-"
                                 + str(self.date.month) + "-"
                                 + str(self.date.day) + " "
                                 + str(hour) + ":"
                                 + str(minute) + ":"
                                 + str(second), '%Y-%m-%d %H:%M:%S')

    def generate_log_in_cycle(self, log_time, name):
        """
        Simulates log in of a user. This user has a chance to miss type his password.
        This chance is determined in the CHANCE_TO_FUCK_UP constant.
        
        :param log_time: 
        :param name: 
        :return: 
        """
        login_log = []
        time_delta = timedelta(seconds=randint(5, 15))

        while True:
            if not self.simulate_chance(self.CHANCE_TO_FUCK_UP):
                login_log.append([log_time, name, 1, 1])
                break

            login_log.append([log_time, name, 0, 1])

            log_time += time_delta

        return login_log

    def generate_hour_cycle(self, hour, names):
        """
        Generates on hour cycle of logs.
        
        :param hour: The hour of the day to generate the log for.
        :param names: List of names.
        :return: A log of a single hour in a list.
        """
        hour_log = []

        for time in range(0, self.random_with_deviation(self.HOUR_SHEET[hour])):
            log_time = self.generate_datetime(hour)

            hour_log.extend(self.generate_log_in_cycle(log_time, self.rand_name(names)))

        return hour_log

    def generate_day_cycle(self, names):
        """
        Generates one day cycle of logs.
        
        :param names: A list of names to be randomly added to the logs.
        :return: A log of a single day cycle in a list.
        """
        day_log = []
        time_delta = timedelta(days=1)

        for i in range(0, len(self.HOUR_SHEET)):
            if self.is_time_for_bruteforce(i):
                day_log.extend(self.generate_brute_force_log(i, names))

            day_log.extend(self.generate_hour_cycle(i, names))

        day_log.sort()

        self.date += time_delta

        return day_log

    def export_to_csv(self, log):
        """
        Generates a CSV file of the log list.
        
        :param log: The log list.
        """
        if os.path.isfile(self.GENERATE_FILE):
            os.remove(self.GENERATE_FILE)

        with open(self.GENERATE_FILE, "w") as f:
            f.write("date, time, username, succes, label\n")

            for entry in log:
                f.write(str(entry[0].date()) + ", "
                        + str(self.hms_to_seconds(entry[0])) + ", "
                        + str(entry[1]) + ", "
                        + str(entry[2]) + ", "
                        + str(entry[3])
                        + "\n")

    def export_group_log_to_csv(self, group_log):
        if os.path.isfile(self.GENERATE_FILE):
            os.remove(self.GENERATE_FILE)

        with open(self.GENERATE_FILE, "w") as f:
            f.write("amount, username, label\n")

            for entry in group_log:
                for key, value in entry.items():
                    label = 1

                    if len(value) > 10:
                        label = 0

                    f.write(str(len(value)) + ", "
                            + str(key) + ", "
                            + str(label)
                            + "\n")

    def generate_days(self, nr_of_days):
        """
        Generates multiple day cycles.
        
        :param nr_of_days: Number of day cycles to generate.
        :return: A log containing multiple day cycles.
        """
        log = []
        names = self.load_names()

        for i in range(0, nr_of_days):
            log.extend(self.generate_day_cycle(names))

        return log

    def hms_to_seconds(self, t):
        h, m, s = [int(i) for i in str(t.time()).split(':')]
        return 3600 * h + 60 * m + s

    def group_log_per_time(self, log, per_time):
        days = self.extract_log_to_day(log)

        per_time_log_list = []
        per_time_log = {}

        for day in days:
            seconds = self.hms_to_seconds(day[0][0])

            for entry in day:
                if self.hms_to_seconds(entry[0]) <= seconds + per_time:
                    if not entry[1] in per_time_log:
                        per_time_log[entry[1]] = []

                    per_time_log[entry[1]].append(entry)
                else:
                    seconds = self.hms_to_seconds(entry[0])

                    per_time_log_list.append(dict(per_time_log))
                    per_time_log.clear()

                    if not entry[1] in per_time_log:
                        per_time_log[entry[1]] = []

                    per_time_log[entry[1]].append(entry)

        return per_time_log_list


    def extract_log_to_day(self, log):
        current_day = log[0][0].date()

        day = []
        days = []

        for entry in log:
            if entry[0].date() == current_day:
                day.append(entry)
            else:
                current_day = entry[0].date()

                days.append(list(day))
                day.clear()
                day.append(entry)

        return days

    def extract_different_users(self, log):
        users = []

        for l in log:
            if not any(l[1] in u for u in users):
                users.append(l[1])

        return users



# Code to run:
g = Generator()

log = g.generate_days(500)

g.export_group_log_to_csv(g.group_log_per_time(log, 1000))