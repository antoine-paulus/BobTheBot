from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions.API.geo_api_handler import *
import backlogs.ivi as ivi




class ActionGEO(Action):

    def __init__(self) -> None:
        super().__init__()
        name = "Agent_geo"
        self.agent = ivi.Agent(name)
        self.geoAPI = GeoApiHandler("Default_name")
        print(f"agent {name} initialised")

    def name(self) -> Text:
        return "action_INIT"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')
        entity = tracker.latest_message['entities'][0]['value']

        question = self.geoAPI.get_question()
        reponses = self.geoAPI.get_choices()

        print(reponses)
        self.agent.send_message(topic="GEO",message=f"{question}/{reponses[0]}/{reponses[1]}/{reponses[2]}/{reponses[3]}")
        return []


if __name__ == "__main__" :
    a = ActionGEO()
    a.run()