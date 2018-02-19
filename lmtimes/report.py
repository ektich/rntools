#!/usr/bin/env python3

import re
import fileinput


cities = ('Moscow', 'Kiev', 'Donetsk', 'St. Petersburg', 'Minsk')
daily_counters = {}
totals = {}


def main():
    weekday = re.compile(">(?P<weekday>\w+) (?P<day>\d+) \w+<")
    announce = re.compile("- (?P<time>[\d:]+) (?P<city>{})".format(
        "|".join(cities)))
    for line in fileinput.input():
        line = line.strip()
        m1 = weekday.match(line)
        m2 = announce.match(line)
        if m1:
            # print(m1.group('weekday'), m1.group('day'))
            cur_day = m1.group('day')
            if cur_day not in daily_counters:
                daily_counters[cur_day] = {}
        if m2:
            # print(m2.group('time'), m2.group('city'))
            if m2.group('city') not in daily_counters[cur_day]:
                daily_counters[cur_day][m2.group('city')] = 1
            else:
                daily_counters[cur_day][m2.group('city')] += 1

            if m2.group('city') not in totals:
                totals[m2.group('city')] = 1
            else:
                totals[m2.group('city')] += 1

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
if __name__ == '__main__':
    main()
