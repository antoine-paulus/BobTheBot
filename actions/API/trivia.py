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
        self.categories = []
        self.userAnswer = ''
        self.url = f'https://the-trivia-api.com/api/questions?limit=1&difficulty={self.difficulty}'
        if self.category != '':
            self.url += f'&categories={self.category}'

    # todo
    # figure out how to change the difficulty of questions

    def load_data(self):
        data = requests.get(self.url)
        json_data = json.loads(data.text)[0]
        self.question = json_data['question']
        self.correctAnswer = json_data['correctAnswer']
        self.incorrectAnswers = json_data['incorrectAnswers']
        self.category = json_data['category']
        self.difficulty = json_data['difficulty']
        self.all_categories = json.loads(requests.get('https://the-trivia-api.com/api/categories').text).keys()
        self.choices = self.incorrectAnswers
        self.choices.append(self.correctAnswer)
        random.shuffle(self.choices)
        for i in range(len(self.choices)):
            if self.choices[i] == self.correctAnswer:
                self.correctAnswer_1234 = str(i+1)
                self.correctAnswer_ABCD = to_letter(i)

    def get_question(self):
        return self.question

    def get_choices(self):
        return self.choices

    def get_correct_answer(self):
        return self.correctAnswer

    def get_correct_answer_ABCD(self):
        return self.correctAnswer_ABCD

    def get_correct_answer_1234(self):
        return self.correctAnswer_1234

    def get_incorrect_answers(self):
        return self.incorrectAnswers

    def set_user_answer(self, answer):
        self.userAnswer = answer

    def get_all_categories(self):
        return self.all_categories

    def get_user_answer(self):
        return self.userAnswer

    def verify_answer(self):
        return self.userAnswer == self.correctAnswer or self.userAnswer == self.correctAnswer_ABCD or self.userAnswer == self.correctAnswer_1234


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
