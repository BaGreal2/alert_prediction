import re


def convert_duration(duration_string):
    hours_pattern = r"(\d+)\s*годин[иу]"
    minutes_pattern = r"(\d+)\s*хвилин[и]?"

    hours_match = re.search(hours_pattern, duration_string)
    minutes_match = re.search(minutes_pattern, duration_string)

    hours = int(hours_match.group(1)) if hours_match else 0
    minutes = int(minutes_match.group(1)) if minutes_match else 0

    seconds = hours * 3600 + minutes * 60
    return seconds
