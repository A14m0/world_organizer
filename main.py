#!/usr/bin/env python3
import json

low_complexity = 1
med_complexity = 2
high_complexity = 3

class bcolors:
    HEADER = '\033[95m'
    CYAN = '\033[0;36m'
    DARKRED = '\033[0;31m'
    YELLOW = '\033[0;33m'
    BRIGHTYELLOW = '\033[1;33m'
    PURPLE = '\033[0;35m'
    BRIGHTPURPLE = '\033[1;35m\033[1;41m'
    BLUE = '\033[0;34m'
    BRIGHTBLUE = '\033[1;34m'
    BLACK = '\033[0;30m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    BACK_RED = '\033[0;41m'
    BACK_BRIGHTRED = '\033[1;41m'
    BACK_GREEN = '\033[0;42m'
    BACK_BRIGHTGREEN = '\033[1;42m'
    BACK_YELLOW = '\033[0;43m'
    BACK_BRIGHTYELLOW = '\033[1;43m'
    BACK_BLUE = '\033[0;44m'
    BACK_BRIGHTBLUE = '\033[1;44m'
    BACK_PURPLE = '\033[0;45m'
    BACK_BRIGHTPURPLE = '\033[1;45m'
    BLACK_RED = '\033[0;30m\033[1;41m'

f = open("questions.json", "r")
dat = f.read()
f.close()

questions = json.loads(dat)


def full_char():
    ret_str = ""
    for question in questions["Questions"]:
        answer = input(question["QuestionString"] + " > ")
        ret_str += "%s: %s\n" % (question["QuestionString"], answer)
    print("\n" * 4)
    print("-"*20)
    print("Generated character information: ")
    print(ret_str)

def med_char():
    ret_str = ""
    for question in questions["Questions"]:
        if question["Priority"] != 3:
            answer = input(question["QuestionString"] + " > ")
            ret_str += "%s: %s\n" % (question["QuestionString"], answer)
    print("\n" * 4)
    print("-"*20)
    print("Generated character information: ")
    print(ret_str)
    return

def min_char():
    ret_str = ""
    for question in questions["Questions"]:
        if question["Priority"] == 1:
            answer = input(question["QuestionString"] + " > ")
            ret_str += "%s: %s\n" % (question["QuestionString"], answer)
    print("\n" * 4)
    print("-"*20)
    print("Generated character information: ")
    print(ret_str)
    return



def main():
    levl = input("How in depth would you like to go? (1 (low), 2 (moderate), 3 (high)) > ")
    try:
        levl = int(levl)
    except Exception as e:
        print("Failed to determine complexity. Please enter a valid complexity level")
        return
    if levl == low_complexity:
        min_char()
    elif levl == med_complexity:
        med_char()
    else:
        full_char()


if __name__ == "__main__":
    main()
