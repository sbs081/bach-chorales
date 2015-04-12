#!/usr/bin/env python
from collections import defaultdict

import csv


def read_data():
    with open('result.csv') as csvfile:
        reader = csv.reader(csvfile)
        reader.next()
        return [row for row in reader]


def group_by_voice():
    dic = defaultdict(list)
    for item in read_data():
        dic[item[1]].append(item)

    return dic


def report():
    dic = group_by_voice()

