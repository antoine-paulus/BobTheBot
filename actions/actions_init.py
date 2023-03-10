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
        entity = tracker.latest_message['entities'][0]['value']

        print(f"\nintent = {intent}\n")

        if intent == "give_name" :

            name_in_db = False

            if name_in_db :
                dispatcher.utter_message(text=f"Welcome back ! What do you want to do.")
            else:
                dispatcher.utter_message(text=f"Hello {entity} nice to meet you ! I am Bob your personnal assistant. If you ever need help just say help or help followed by the activity you need more information about. What do you want to do ?")


        else:
            dispatcher.utter_message(text=f"Debug : custom action from intent={intent}")
        

        return []

