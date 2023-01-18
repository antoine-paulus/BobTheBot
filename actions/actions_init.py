# This files contains a custom actions which is used 
# to run the correct function according to the user intent.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionINIT(Action):

    def __init__(self) -> None:
        super().__init__()
        print("init1")
    
    def name(self) -> Text:
        return "action_INIT"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        print("action1")
        print(f"\nintent = {intent}\n")

        if intent == "give_name" :
            name = "Bastian"

            pass
        else:
            dispatcher.utter_message(text=f"Debug : custom action from intent={intent}")
        

        return []

