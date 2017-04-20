import re

ip_list = []
time_list = []
bool_list = []

with open("./auth.log") as the_file:
    for line in the_file:
        if re.search(r'Failed password', line):
            time_list.append(re.findall(r'[0-9]+(?:\:[0-9]+){2}', line))
            ip_list.append(re.findall(r'[0-9]+(?:\.[0-9]+){3}', line))
            bool_list.append(0)
        elif re.search(r'Accepted password', line):
            time_list.append(re.findall(r'[0-9]+(?:\:[0-9]+){2}', line))
            ip_list.append(re.findall(r'[0-9]+(?:\.[0-9]+){3}', line))
            bool_list.append(1)

with open("./ssh-log.csv", "w") as the_file:
    max = len(ip_list)
    the_file.write("time, ip, succes \n")

    for i in range(0, max):
        the_file.write(str(time_list[i][0]) + ", "
                       + str(ip_list[i][0]) + ", "
                       + str(bool_list[i])
                       + "\n")
