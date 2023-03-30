import json
import datetime as dt
from utils import convert_time, get_status


class AlertStruct:
    def __init__(self, start_date, end_date=-1):
        self.start_date = start_date
        self.end_date = end_date


class AlertsDayGrouped:
    def __init__(self, date, alerts):
        self.date = date
        self.alerts = alerts


with open('alerts.json', 'r') as alerts_file:
    alerts_data = json.load(alerts_file)[0]


def get_alerts(data):
    alerts_arr = []
    for i in reversed(range(len(data["date"]))):
        date_str = data["date"][i]
        date = convert_time(date_str)
        if (date.year == 2022):
            continue

        state = data["state"][i]
        is_alert = get_status(state)

        if (is_alert):
            alerts_arr.append(AlertStruct(date))

        else:
            # if it's vidbiy and alert in one day
            if (alerts_arr[-1].start_date.day == date.day and alerts_arr[-1].start_date.month == date.month):
                alerts_arr[-1].end_date = date
            # if it's vidbiy and alert is split
            else:
                prev_day_start = alerts_arr[-1].start_date
                prev_day_end = dt.datetime(
                    prev_day_start.year, prev_day_start.month, prev_day_start.day, 23, 59)

                next_day_start = dt.datetime(
                    date.year, date.month, date.day, 0, 0)
                next_day_end = date
                alerts_arr[-1].end_date = prev_day_end
                alerts_arr.append(AlertStruct(next_day_start, next_day_end))
    return alerts_arr


def group_alerts(alerts_arr):
    alerts_grouped = []
    for i in range(len(alerts_arr)):
        curr_alert = alerts_arr[i]
        indexes = [j for j in range(len(alerts_grouped))
                   if (alerts_grouped[j].date.month == curr_alert.start_date.month) and (alerts_grouped[j].date.day == curr_alert.start_date.day)]
        if (not (bool(indexes))):
            start_date = curr_alert.start_date
            grouped_date = dt.datetime(
                start_date.year, start_date.month, start_date.day)
            alerts_grouped.append(AlertsDayGrouped(grouped_date, [curr_alert]))
        else:
            idx = indexes[0]
            alerts_grouped[idx].alerts.append(curr_alert)

    return alerts_grouped


def amound_of_weekday(weekday):
    count = 0
    curr_date = dt.datetime(2023, 1, 1)
    end_date = dt.datetime.now()

    while curr_date <= end_date:
        if (curr_date.weekday() == weekday):
            count += 1
        curr_date += dt.timedelta(days=1)

    return count


def get_weekday_alerts(weekday, all_grouped_alerts):
    return [alert_day for alert_day in all_grouped_alerts if alert_day.date.weekday() == weekday]


def calculate_for_weekday(weekday, all_grouped_alerts):
    weekday_alerts = get_weekday_alerts(weekday, all_grouped_alerts)

    return len(weekday_alerts) / amound_of_weekday(weekday)


def calculate_for_hours_in_weekday(weekday, all_grouped_alerts):
    hours = [i for i in range(24)]
    hours_prob = []

    for hour in hours:
        hours_prob.append(calculate_for_hour(hour, weekday, all_grouped_alerts))

    return hours_prob


def calculate_for_hour(hour, weekday, all_grouped_alerts):
    weekday_alerts = get_weekday_alerts(weekday, all_grouped_alerts)
    weekday_all = amound_of_weekday(weekday)
    weekday_alert_prob = calculate_for_weekday(weekday, all_grouped_alerts)

    alerts_in_hour = 0
    for alert_day in weekday_alerts:
        for alert in alert_day.alerts:
            if(alert.end_date.hour >= hour and alert.start_date.hour <= hour):
                alerts_in_hour += 1

    return (weekday_alert_prob * alerts_in_hour / weekday_all)


probability_for_week = []
alerts_arr = get_alerts(alerts_data)
alerts_grouped = group_alerts(alerts_arr)

for i in range(7):
    day_prob = calculate_for_weekday(i, alerts_grouped)
    hours_prob = []
    for hour_prob in calculate_for_hours_in_weekday(i, alerts_grouped):
        hours_prob.append(hour_prob)
    probability_for_week.append({
        "day_prob": day_prob,
        "hours_prob": hours_prob
    })

json_string = json.dumps(probability_for_week)

with open("probability_week.json", "w") as outfile:
    outfile.write(json_string)
