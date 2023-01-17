import requests
import json
import webbrowser
from actions.API.keys import APOD_API_KEY

class Nasa:
    def __init__(self):
        self.url = 'https://api.nasa.gov/planetary/apod?api_key=' + APOD_API_KEY
        self.image = ''
        self.description = ''

    def load_data(self):
        data = requests.get(self.url)
        json_data = json.loads(data.text)
        self.image = json_data['hdurl']
        self.description = json_data['explanation']

    def get_image(self):
        return self.image

    def get_description(self):
        return self.description

    def show_image(self):
        webbrowser.open(self.image)


''' 
# Tests
nasa = Nasa()
nasa.load_data()
print(nasa.get_image())
print(nasa.get_description())
nasa.show_image()
# Tests : OK
'''