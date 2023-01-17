# This files contains a custom actions which is used 
# to run the correct function according to the user intent.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions.API.geo_api_handler import GeoApiHandler
from actions.API.nasa import Nasa
from actions.API.trivia import Trivia

from BobDisplay.display import *

class ActionAPI(Action):

    def __init__(self) -> None:
        super().__init__()
        
        # API
        self.geoAPI = GeoApiHandler("Default_name")
        self.nasaAPI = Nasa()
        self.triviaAPI = Trivia()


        # Pygame display
        self.display_queue = multiprocessing.Queue()
        self.display_process = multiprocessing.Process(target=display_Bob, args=(self.display_queue,))
        self.display_process.start()


    def name(self) -> Text:
        return "action_API"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')

        print(f"\nintent = {intent}\n")

        if intent == "geography" :
            question = self.geoAPI.generate_question()
            print(question)
            dispatcher.utter_message(text=question)

        elif intent == "trivia" :
            self.display_queue.put(b"trivia")
            dispatcher.utter_message(text=f"Debug : custom action n°{self.iter} intent={intent}")

        elif intent == "nasa" :
            self.display_queue.put(b"nasa")
            image = self.nasaAPI.get_image()
            print(image)
            text = self.nasaAPI.get_description()
            print(text)
            dispatcher.utter_message(text=f"Debug : custom action n°{self.iter} intent={intent}")

        else:
            dispatcher.utter_message(text=f"Debug : custom action n°{self.iter} intent={intent}")


        self.iter += 1
        

        return []

