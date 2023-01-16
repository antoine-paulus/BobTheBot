# This files contains a custom actions which is used 
# to run the correct function according to the user intent.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionAPI(Action):

    iter = 0

    #geoAPI = ...
    #triviaAPI = ...
    #nasaAPI = ...

    def __init__(self) -> None:
        super().__init__()
        self.iter = 0
        #self.geoAPI = ...
        #self.triviaAPI = ...
        #self.nasaAPI = ...

    def name(self) -> Text:
        return "action_API"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')

        print(f"\nintent = {intent}\n")

        if intent == "geo" :
            pass
        elif intent == "trivia" :
            pass
        elif intent == "nasa" :
            pass


        self.iter += 1
        dispatcher.utter_message(text=f"Hello World! n°{self.iter}")

        return []

