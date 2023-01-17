import random
import requests
import json


def to_letter(i):
    if i == 0:
        return 'A'
    elif i == 1:
        return 'B'
    elif i == 2:
        return 'C'
    else:
        return 'D'


class Trivia:
    def __init__(self, difficulty='easy', category=''):
        self.question = ''
        self.correctAnswer = ''
        self.incorrectAnswers = ''
        self.choices = []
        self.correctAnswer_ABCD = ''
        self.correctAnswer_1234 = ''
        self.difficulty = difficulty
        self.category = category
        self.all_categories = json.loads(requests.get('https://the-trivia-api.com/api/categories').text).keys()
        self.categories = []
        self.url = f'https://the-trivia-api.com/api/questions?limit=1&difficulty={self.difficulty}'
        if self.category != '':
            self.url += f'&categories={self.category}'

    def get_question(self):
        return self.question

    def get_choices(self):
        return self.choices

    def generate_question(self, difficulty='easy', category=''):
        self.update_settings(difficulty, category)
        data = requests.get(self.url)
        json_data = json.loads(data.text)[0]
        self.question = json_data['question']
        self.correctAnswer = json_data['correctAnswer']
        self.incorrectAnswers = json_data['incorrectAnswers']
        self.choices = self.incorrectAnswers
        self.choices.append(self.correctAnswer)
        random.shuffle(self.choices)
        for i in range(len(self.choices)):
            if self.choices[i] == self.correctAnswer:
                self.correctAnswer_1234 = str(i+1)
                self.correctAnswer_ABCD = to_letter(i)

    def get_result(self, answer):
        if answer == self.correctAnswer or answer == self.correctAnswer_ABCD \
                or answer == self.correctAnswer_1234:
            if self.difficulty == 'easy':
                return True, 1, "Yes, your answer is correct! You have earned 1 point."
            elif self.difficulty == 'medium':
                return True, 2, "Yes, your answer is correct! You have earned 2 points."
            else:
                return True, 3, "Yes, your answer is correct! You have earned 3 points."
        else:
            return False, 0, f"Ops, your answer is wrong! The correct answer was : {self.correctAnswer}"

        def get_all_categories(self):
            return self.all_categories

        def update_settings(self, difficulty, category):
            self.difficulty = difficulty
            self.category = category
            self.url = f'https://the-trivia-api.com/api/questions?limit=1&difficulty={self.difficulty}'
            if self.category != '':
                self.url += f'&categories={self.category}'

"""

    def get_correct_answer_ABCD(self):
        return self.correctAnswer_ABCD

    def get_correct_answer_1234(self):
        return self.correctAnswer_1234

    def get_incorrect_answers(self):
        return self.incorrectAnswers
"""

'''
# Tests
trivia = Trivia(difficulty='hard', category='geography,science')
trivia.load_data()
print(trivia.get_all_categories())
print(trivia.url)
print(trivia.get_question())
print(trivia.get_choices())
print(trivia.difficulty)
print(trivia.category)
trivia.set_user_answer(trivia.get_choices()[1])
print(trivia.get_user_answer())
print(trivia.verify_answer())
if not(trivia.verify_answer()):
    print(f"The correct answer was : {trivia.get_correct_answer()} or {trivia.get_correct_answer_ABCD()} or {trivia.get_correct_answer_1234()}")
# Tests : OK
'''

