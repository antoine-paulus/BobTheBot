import random
import requests
import json


class Trivia:
    def __init__(self):
        self.url = 'https://the-trivia-api.com/api/questions?limit=1'
        self.question = ''
        self.correctAnswer = ''
        self.incorrectAnswers = ''
        self.choices = []
        self.userAnswer = ''

        # self.difficulty = ''

    # todo
    # figure out how to change the difficulty of questions

    def load_data(self):
        data = requests.get(self.url)
        json_data = json.loads(data.text)[0]
        self.question = json_data['question']
        self.correctAnswer = json_data['correctAnswer']
        self.incorrectAnswers = json_data['incorrectAnswers']
        self.choices = self.incorrectAnswers
        self.choices.append(self.correctAnswer)
        random.shuffle(self.choices)

    def get_question(self):
        return self.question

    def get_choices(self):
        return self.choices

    def get_correct_answer(self):
        return self.correctAnswer

    def get_incorrect_answers(self):
        return self.incorrectAnswers

    def set_user_answer(self, answer):
        self.userAnswer = answer

    def get_user_answer(self):
        return self.userAnswer

    def verify_answer(self):
        return self.userAnswer == self.correctAnswer

"""
# Tests
trivia = Trivia()
trivia.load_data()
print(trivia.get_question())
print(trivia.get_choices())
trivia.set_user_answer(trivia.get_choices()[1])
print(trivia.get_user_answer())
print(trivia.verify_answer())
if not(trivia.verify_answer()):
    print(f"The correct answer was : {trivia.get_correct_answer()}")
# Tests : OK
"""