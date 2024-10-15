#!usr/bin/env python3
import json
import sys
import os

INPUT_FILE = 'testdata.json' # Constant variables are usually in ALL CAPS

class User:
    def __init__(self, name, gender, preferences, grad_year, responses):
        self.name = name
        self.gender = gender
        self.preferences = preferences
        self.grad_year = grad_year
        self.responses = responses


# Takes in two user objects and outputs a float denoting compatibility
def compute_score(user1, user2):
    score = 0
    # Check gender preferences first
    if user1.gender not in user2.preferences or user2.gender not in user1.preferences:
        print("{} and {} do not align in terms of gender preferences".format(user1.name, user2.name))
        return 0
    
    # Check grade years, we don't want them to more than two years apart
    if abs(user1.grad_year - user2.grad_year) > 2:
        print("{} and {} are over two years apart...making sure we don't catch a case".format(user1.name, user2.name))
        return 0
    else:
        # depending on their year, add a certain amount of points
        if user1.grad_year == user2.grad_year:
            score += 20 
        elif abs(user1.grad_year - user2.grad_year) > 1:
            score += 10 
        else:
            score += 5

    # for every question in the responses array that is the same, they get four points
    total_questions = len(user1.responses)
    for i in range(total_questions):
        if user1.responses[i] == user2.responses[i]:
            score += 4
    # divide by 100 to normalize the score between 0-1
    # the max score two users could have is 100 -- 80 from the matching responses (4 x 20) + 20 from being in the same grade
    return (score/100)


if __name__ == '__main__':
    # Make sure input file is valid
    if not os.path.exists(INPUT_FILE):
        print('Input file not found')
        sys.exit(0)

    users = []
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for user_obj in data['users']:
            new_user = User(user_obj['name'], 
                            user_obj['gender'],
                            user_obj['preferences'], 
                            user_obj['gradYear'],
                            user_obj['responses'])
            users.append(new_user)

    for i in range(len(users)-1):
        for j in range(i+1, len(users)):
            user1 = users[i]
            user2 = users[j]
            score = compute_score(user1, user2)
            print('Compatibility between {} and {}: {}\n'.format(user1.name, user2.name, score))