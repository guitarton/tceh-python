#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

QUESTION, ANSWER = 0, 1

question_answers = (
    ("Is python a case sensitive language?(true or false)", "true"),
    ("What is the output of print str[0] if str = 'Hello World!'?", "H"),
    ("Which operator in python performs exponential (power) calculation on operands?", "**")
)

count_wrong = 0
input_function = raw_input if sys.version_info[0] == 2 else input


def check_answer(question, answer):
    return input_function(question) == answer


for qa in question_answers:
    while True:
        if check_answer(qa[QUESTION], qa[ANSWER]):
            break
        else:
            print("Error! Try harder!")
            count_wrong += 1

print("Congratulations! You've done {} error(s)!".format(count_wrong))
