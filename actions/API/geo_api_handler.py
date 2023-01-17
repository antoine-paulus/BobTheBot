import pycountry
from random import randint
import requests
import json
from actions.API.keys import GEO_API_KEY

class GeoApiHandler:

    def __init__(self, name : str):
        self._countries_list = list(pycountry.countries)
        self.current_question = ""
        self.current_answer = ""
        self.current_user_score = 0


    def _get_random_country(self):
        """Return a random country alpha 3 code from all available countries"""
        return self._countries_list[randint(0, len(self._countries_list ) - 1)].alpha_3


    def _get_country_flag(self, country_name : str):
        """Get the flag of the specified country"""
        print("")
        response = requests.get(f"https://countryflagsapi.com/png/{country_name}")


    def _get_country_data(self, country_name : str) -> dict:
        """"""

        data = {}
        headers= {
        "apikey": GEO_API_KEY
        }
        response = requests.get(f"https://api.apilayer.com/geo/country/name/{country_name}", headers=headers)
        if response.status_code == 200:
            response_dict = response.json()[0]
            data["name"] = response_dict["name"]
            data["capital"] = response_dict["capital"]
            data["continent"] = response_dict["region"]
            data["currencies"] = response_dict["currencies"][0]["name"]
            data["language"] = response_dict["languages"][0]["name"]
            data["flag"] = response_dict["flag"]
        else:
            print(f"An error occured when retrieving data for {country_name} country")
        return data
    

    def generate_question(self) -> str:
        #Get a random country:

        country_code = self._get_random_country()
        country_data = self._get_country_data(country_code)
        country_name = country_data["name"]
        data_type_list = list(country_data.keys())
        #data_type_list = ["flag"]
        data_type = data_type_list[randint(0, len(data_type_list) - 1)]
        if data_type == "flag":
            self._get_country_flag(country_data["flag"])
            self.current_question = "To what country this flag is ?"
            self.current_answer = country_name
        else:
            self.current_question = f"What is the {data_type} of {country_name} ?"
            self.current_answer = country_data[data_type]
        return self.current_question


    def check_answer(self, given_answer : str) -> None:
        """"""

        if self.current_answer in given_answer :
            self.current_user_score += 1
            return f"Great this is the good answer ! Your score is {self.current_user_score}"
        else:
            self.current_user_score = 0
            return f"No sorry, the correct answer is {self.current_answer}"


if __name__ == '__main__':
    geo_handler = GeoApiHandler("Bob")
    print(geo_handler.generate_question())
    response = str(input())
    print(geo_handler.check_answer(response))
