#!/usr/bin/env python3

import re
import fileinput
import pandas as pd

cities = ('Moscow', 'Kiev', 'Donetsk', 'St. Petersburg', 'Minsk')
daily_counters = {}
totals = {}
timeline = list()
switch = list()
allocated_hours = list()


def process_file(file):
    current_city = None
    switch_timestamp = None
    weekday = re.compile(">(?P<weekday>\w+) (?P<day>\d+) (?P<month>\w+)<")
    announce = re.compile("- (?P<time>[\d:]+) (?P<city>{})".format(
        "|".join(cities)))
    for line in fileinput.input(file):
        line = line.strip()
        m1 = weekday.match(line)
        m2 = announce.match(line)
        if m1:
            # day change record
            print(m1.group('weekday'), m1.group('day'), m1.group('month'))
            current_day = "{}-{}-{}".format(2018,
                                            m1.group('month'),
                                            m1.group('day'))
            # current_day is used when calculating timestamps
            if current_day not in daily_counters:
                daily_counters[current_day] = {}
        if m2:
            # switch record detected.
            # 1. calculate the difference in time stamps
            new_timestamp = pd.Timestamp("{} {}".format(current_day,
                                                        m2.group('time')))
            if switch_timestamp is not None:
                delta = new_timestamp - switch_timestamp
                # insert delta into hours.
                allocated_hours.append(delta)

            switch_timestamp = new_timestamp
            # current_city
            # 2. add the amount of hours to the city LM is taken away from
            # 3. update variables such as "switch_timestamp" and "current_city"

            print(m2.group('time'))
            # print(m2.group('time'), m2.group('city'))
            # adding detected time to a timeline
            timeline.append(pd.Timestamp("{} {}".format(current_day,
                                                        m2.group('time'))))
            switch.append(m2.group('city'))
            if m2.group('city') not in daily_counters[current_day]:
                daily_counters[current_day][m2.group('city')] = 1
            else:
                daily_counters[current_day][m2.group('city')] += 1

            if m2.group('city') not in totals:
                totals[m2.group('city')] = 1
            else:
                totals[m2.group('city')] += 1
    # reached end of file: last city just got the bonus, assign 0 hours
    allocated_hours.append(0)


def main():
    process_file('LM_changes_180224.txt')
    # checks: each day should have 6 slots
    for k in daily_counters.keys():
        check = 0
        for city, hours in daily_counters[k].items():
            check = check + hours
        if check != 6:
            print("problem with {}: {}".format(k, daily_counters[k]))
    # print(counters)
    for k, d in daily_counters.items():
        print("{} Feb".format(k))
        for c, h in d.items():
            print("  {}: {} hours".format(c, h*4))

    for k, d in totals.items():
        print("{}: {} hours".format(k, d*4))

    # combine timeline and switch into a dataframe
    print(len(switch))
    print(len(allocated_hours))
    print(len(timeline))
    df = pd.DataFrame({'City': switch, 'Hours': allocated_hours},
                      index=timeline)

    print(df)


if __name__ == '__main__':
    main()
