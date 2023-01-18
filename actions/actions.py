# This files contains a custom actions which is used 
# to run the correct function according to the user intent.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions.API.geo_api_handler import *
from actions.API.nasa import Nasa
from actions.API.trivia import Trivia

from BobDisplay.display import *

class ActionAPI(Action):

    def __init__(self) -> None:
        super().__init__()
        
        # API
        self.geoAPI = GeoApiHandler("Default_name")
        self.nasaAPI = Nasa()
        self.nasaAPI.load_data()
        self.triviaAPI = Trivia()
        self.triviaAPI.generate_question()


        # Pygame display
        self.display_queue = multiprocessing.Queue()
        self.display_process = multiprocessing.Process(target=display_Bob, args=(self.display_queue,))
        self.display_process.start()
        self.nb_question = 0

    def name(self) -> Text:
        return "action_API"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')

        print(f"\nintent = {intent}\n")

        if intent == "geography" :
            self.display_queue.put(b"geography")
            type, question = self.geoAPI.generate_question()
            print(f"type={type}, question={question}")
            if type == "flag":
                dispatcher.utter_message(text=question, image=FLAG_IMG_PATH)
            else:
                dispatcher.utter_message(text=question)

        elif intent == "trivia" :
            self.display_queue.put(b"trivia")
            question = self.triviaAPI.get_question()
            dispatcher.utter_message(text=question)
            
            answer = self.triviaAPI.get_choices()
            answers_text = f"A={answer[0]}/B={answer[1]}/C={answer[2]}/D={answer[3]}"
            dispatcher.utter_message(text=answers_text)
        


        elif intent == "nasa" :
            self.display_queue.put(b"nasa")
            image = self.nasaAPI.get_image()
            print("action.py => NASA")
            display_image = "image_nasa "+image
            self.display_queue.put(bytes(display_image, encoding='utf8'))

            txt = self.nasaAPI.get_description()

            dispatcher.utter_message(text = txt)

        else:
            dispatcher.utter_message(text=f"Debug : custom action from intent={intent}")
        

        return []

