import os.path
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
    MAX_NR_OF_ATTACKS = 100000
    BEGIN_DATE = datetime.strptime('2015-05-12', '%Y-%m-%d')
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

    def random_with_deviation(self, number):
        """
        Generates a random number with a random deviation.
        
        :param number: The number to deviate around.
        :return: A random number.
        """
        min_bound = round(number - number / (100 / self.DEVIATION_PERCENTAGE))
        max_bound = round(number + number / (100 / self.DEVIATION_PERCENTAGE))

        return randint(min_bound, max_bound)

    def is_time_for_bruteforce(self, hour):
        """
        Randomly determines if it's time for bruteforce. This depends on the hour of day.
        Change per hour of day is determined in BRUTEFORCE_CHANCE_SHEET.
        
        :param hour: The hour of the day.
        :return: A boolean representing whether or not it's time for bruteforce.
        """
        number_to_guess = randint(0, self.BRUTE_FORCE_CHANCE_SHEET[hour])
        guess = randint(0, self.BRUTE_FORCE_CHANCE_SHEET[hour])

        return number_to_guess == guess

    def generate_brute_force_log(self, hour, names):
        """
        Generates a bruteforce log which begins somewhere in a given hour and ends 
        when a random amount of attacks have been logged.
        
        :param hour: The hour in which the attacks begin.
        :param names: A list of names.
        :return: A list containing the log of the attack.
        """
        time = self.generate_datetime(hour)
        d = timedelta(seconds=1)
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
            time += d

        return log

    def rand_name(self, names):
        """
        Gets a random name from the list of names
        
        :param names:  The list of names.
        :return: A random name from the list.
        """
        return names[randint(0, len(names) - 1)]

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
                b_log = self.generate_brute_force_log(i, names)

                for entry in b_log:
                    day_log.append(entry)

            for time in range(0, self.random_with_deviation(self.HOUR_SHEET[i])):
                log_time = self.generate_datetime(i)

                day_log.append([log_time, self.rand_name(names), 1, 1])

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
            f.write("time, username, succes, label\n")

            for entry in log:
                f.write(str(entry[0]) + ", "
                        + str(entry[1]) + ", "
                        + str(entry[2]) + ", "
                        + str(entry[3])
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
            day_log = self.generate_day_cycle(names)

            for entry in day_log:
                log.append(entry)

        return log


# Code to run:
g = Generator()

log = g.generate_days(365)

g.export_to_csv(log)
