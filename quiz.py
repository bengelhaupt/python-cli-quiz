import sys
import json
import random

def main():
    if len(sys.argv) < 2:
        print("Please start with python %s [QUESTION FILE]" % (sys.argv[0]))
        exit(1)
    
    questions = load_questions_from_file(sys.argv[1])
    
    mode = ask_for_mode()
    print()
    
    jokers = ["5050", "audience", "phone", "risk"]
    if mode == "safe":
        jokers.remove("risk")
        
    for num in range(0,14): #this means 15 questions
        index = get_next_question(questions, num)
        if not ask_question(questions, index, jokers):
            end(num, mode)
    
    end(14, mode)

def ask_for_mode():
    mode = ""
    while mode != "s" and mode != "r":
        mode = input("Welcome to the Quiz! Safe or Risk? Type s or r and hit Enter\t")
        
    if mode == "s":
        print("You have chosen safe mode")
        return "safe"
    else:
        print("you have chosen risk mode")
        return "risk"

    
def load_questions_from_file(filename):
    question_file = open(filename)
    question_str = question_file.read()
    return json.loads(question_str)["questions"]
    
def get_next_question(questions, points):
    return random.randrange(0, 15) #take care of difficulty
    
def ask_question(questions, index, jokers):
    question = questions.pop(index)
    print(question["question"])
    options = question["options"]
    for option_index in range(0, len(options)):
        print("%i) %s" % (option_index, options[option_index]))
    
    reply = -1
    while reply < 0 or reply >= len(options):
        reply = input("What is the answer? Type it's number or j (Joker) and hit Enter\t")
        if reply == "j":
            joker = select_joker(jokers)
            execute_joker(joker, question)
        try:
            reply = int(reply)
        except:
            reply = -1
            
    if reply == question["answer"]:
        print("Correct!\r\n")
        return True
    else:
        print("Wrong!\r\n")
        return False

def select_joker(jokers):
    if len(jokers) == 0:
        print("You have no jokers left.")
        return ""
    
    joker = ""
    while joker not in jokers:
        print("Select a joker. You have the following left:")
        for j in jokers:
            print(j)
        joker = input("Type the name of the joker and press Enter\t")
    jokers.remove(joker)
    print("You have chosen the %s joker" % (joker))
    return joker
    
def execute_joker(joker, question):
    if joker == "5050":
        fiftyfifty(question)
    elif joker == "audience":
        audience(question)
    elif joker == "phone":
        phone(question)
    elif joker == "risk":
        risk(question)
    else:
        print("You have no jokers left")

def fiftyfifty(question):
    remaining_options = []
    while question["options"][question["answer"]] not in remaining_options:
        remaining_options = random.sample(question["options"], int(len(question["options"])/2))
    print("The following options remain:")
    for option in remaining_options:
        print(option)
        
def audience(question):
    print("The audience thinks it is %s" % (question["options"][question["answer"]])) #invent some logic here and use difficulty
    
def phone(question):
    print("I thinks it is %s" % (question["options"][question["answer"]])) #invent some logic here and use difficulty
    
def risk(question):
    print("I thinks it is %s" % (question["options"][question["answer"]])) #invent some logic here and use difficulty

def end(points, mode):
    print("You answered %i questions correct" % (points))
    if mode == "safe" and points > 7:
        print("You got 16000")
    print("You have won XXX Euro") # build a scheme here
    exit(0)


if __name__== "__main__":
    main()