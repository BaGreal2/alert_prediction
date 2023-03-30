import re
import datetime as dt


def convert_time(time_string):
    regex = r"(\d{2}:\d{2})\s+(\d{2}\.\d{2}\.\d{2})"

    match = re.search(regex, time_string)

    time_str, date_str = match.group(1), match.group(2)

    date = dt.datetime.strptime(f"{date_str} {time_str}", "%d.%m.%y %H:%M")

    return date


