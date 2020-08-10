#!/usr/bin/env python3
import json
from elements import *

low_complexity = 1
med_complexity = 2
high_complexity = 3


f = open("questions.json", "r")
dat = f.read()
f.close()

questions = json.loads(dat)


def full_char():
    character = Character()
    for question in questions["Questions"]:
        element = Attribute()
        element.set_e1(question["QuestionString"])
        answer = input(question["QuestionString"] + " > ")
        element.set_e2(answer)
        character.add_attribute(element)

    print("\n" * 4)
    print("-"*20)
    print(character)
    

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
