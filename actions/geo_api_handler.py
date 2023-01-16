import pycountry
from random import randint
import requests
import json
import keys

class GeoApiHandler:

    def __init__(self, name : str):
        self._countries_list = list(pycountry.countries)
        self.current_question = ""
        self.current_answer = ""
        self.current_user_score = 0


    def _get_random_country(self):
        """Return a random country name from all available countries"""
        return self.countries_list[randint(0, len(self.countries_list - 1))]


    def _get_country_data(self, country_name : str) -> dict:
        """"""

        data = {}
        headers= {
        "apikey": keys.GEO_API_KEY
        }
        response = requests.get(f"https://api.apilayer.com/geo/country/name/{country_name}", headers=headers)
        if response.status_code == 200:
            response_dict = response.json()[0]
        data["name"] = response_dict["name"]
        data["capital"] = response_dict["capital"]
        data["continent"] = response_dict["region"]
        data["currencies"] = response_dict["currencies"]["name"]
        data["language"] = response_dict["languages"]
        return data
    

    def generate_question(self) -> str:
        """"""

        #Get a random country:
        country_name = self._get_random_country()
        country_data = self._get_country_data(country_name)
        data_type_list = country_data.keys()
        data_type = data_type_list[randint(0, len(data_type_list) - 1)]
        self.current_question = f"What is the {data_type} of {country_name} ?"
        self.current_answer = country_data[data_type]
        return f"What is the {data_type} of {country_name} ?"


    def check_answer(self, given_answer : str) -> None:
        """"""

        if self.current_answer in given_answer :
            self.current_user_score += 1
            return f"Great this is the good answer ! Your score is {self.current_user_score}"
        else:
            self.current_user_score = 0
            return f"No sorry, the correct answer is {self.current_answer}"

if __name__ == '__main__':
    geo_handler = GeoApiHandler()
    geo_handler.get_country_data("France")
