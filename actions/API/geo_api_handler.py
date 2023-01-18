from random import randint
import requests

FLAG_IMG_PATH = "./actions/API/current_flag.png"
NUM_RESPONSES = 4

class GeoApiHandler:

    def __init__(self, user_name : str):
        #Load data from the API rest:
        self._countries_data = {}
        response = requests.get(f"https://restcountries.com/v2/all")
        if response.status_code == 200:
            self._countries_data = response.json()
        else:
            print(f"An error occured when retrieving countries data. Code error : {response.status_code}")

        self.current_country_name = ""
        self.current_data_type = ""
        self.current_question = ""
        self.current_answer = ""
        self._current_answer_index = ""
        self.current_user_score = 0


    def _get_country_flag(self, country_name : str):
        """Get the flag of the specified country"""
        response = requests.get(f"https://countryflagsapi.com/png/{country_name}", timeout=5)
        if response.status_code == 200:
            with open(FLAG_IMG_PATH, 'wb') as flag_img:
               flag_img.write(response.content)
        else:
            print(f"code error {response.status_code}")


    def _get_country_data(self, country_index : int) -> dict:
        """"""

        data = {}
        #Sample random country from the database
        country_data = self._countries_data[country_index]
        data["name"] = country_data["name"]
        data["capital"] = country_data["capital"]
        data["continent"] = country_data["region"]
        data["currency"] = country_data["currencies"][0]["name"]
        data["language"] = country_data["languages"][0]["name"]
        data["alpha3Code"] = country_data["alpha3Code"]
        return data
    

    def _generate_responses(self, country_name : str) -> list:
        """"""

        #Generate possible responses:
        sampled_countries_name = [country_name]
        responses = []
        while len(sampled_countries_name) != NUM_RESPONSES:
            #Sample a random country:
            country_index = randint(0, len(self._countries_data) -1)
            country_data = self._get_country_data(country_index)
            if country_data["name"] not in sampled_countries_name:
                response = country_data[self.current_data_type]
                #To avoid dupplicated responses:
                if response not in responses:
                    sampled_countries_name.append(country_data["name"])
                    #Generate a response
                    responses.append(country_data[self.current_data_type])
        #Insert the right response at a random index in the responses list:
        self._current_answer_index = randint(0, NUM_RESPONSES - 1)
        responses.insert(self._current_answer_index, self.current_answer)
        return responses


    def get_user_score(self):
        return self.current_user_score


    def get_question(self) -> tuple:
        """"""
        if self._countries_data != {}:
             #Get a random country:
            country_index = randint(0, len(self._countries_data) - 1)
            country_data = self._get_country_data(country_index)
            if country_data != {}:
                #Generate question
                self.current_country_name = country_data["name"]
                data_type_list = list(country_data.keys())
                #data_type_list = ["flag"]
                self.current_data_type = data_type_list[randint(0, len(data_type_list) - 1)]
                #We don't want to get 'name'or alphacode for question type:
                while self.current_data_type in ["name", "alpha3Code"]:
                    self.current_data_type = data_type_list[randint(0, len(data_type_list) - 1)]
                #Handle specific case for flag question type:
                if self.current_data_type == "flag":
                    self._get_country_flag(self.current_country_name)
                    self.current_question = "To which country does this flag belong?"
                    self.current_answer = self.current_country_name
                else:
                    self.current_question = f"What is the {self.current_data_type} of {self.current_country_name} ?"
                    self.current_answer = country_data[self.current_data_type]
        return (self.current_data_type, self.current_question)


    def get_choices(self):
        """"""

        responses = self._generate_responses(self.current_country_name)
        choices_str = ""
        choices_letter = ["A:", "B:", "C:", "D:"]
        for (i, letter) in enumerate(choices_letter):
            choices_str += "response " + letter + " " + responses[i] + "\n"
        return choices_str


    def check_answer(self, given_answer : str) -> None:
        """"""

        choices_letter = [" response A", "response B", " response C", "response D"]
        if self.current_answer in choices_letter[self._current_answer_index]:
            self.current_user_score += 1
            return f"Great this is the good answer ! Your score is {self.current_user_score}"
        else:
            self.current_user_score = 0
            return f"No sorry, the correct answer is {self.current_answer}"


if __name__ == '__main__':
    geo_handler = GeoApiHandler("Bob")
    print(geo_handler.get_question())
    print(geo_handler.get_choices())
