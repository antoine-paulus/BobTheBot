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
        self.nb_question_max = 5
        self.current_score = 0
        self.last_activity = ""

    def name(self) -> Text:
        return "action_API"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')

        print(f"\nintent = {intent}\n")

        if intent == "geography" :
            self.display_queue.put(b"geography")
            type, question = self.geoAPI.get_question()
            print(f"type={type}, question={question}")
            if type == "flag":
                dispatcher.utter_message(text=question, image=FLAG_IMG_PATH)
            else:
                dispatcher.utter_message(text=question)
            choices = self.geoAPI.get_choices()
            answers_text = f"{choices[0]} /{choices[1]}  /{choices[2]}  /{choices[3]}"
            self.display_queue.put(bytes("TA/"+answers_text,encoding='utf8'))
            dispatcher.utter_message(text=choices)
            self.last_activity = "gro"
            

        elif intent == "trivia" :
            self.nb_question +=1
            self.display_queue.put(b"trivia")
            question = self.triviaAPI.get_question()
            dispatcher.utter_message(text=question)
            self.display_queue.put(bytes("TQ/"+question,encoding='utf8'))
            
            answer = self.triviaAPI.get_choices()
            answers_text = f"A = {answer[0]}  /B = {answer[1]}  /C = {answer[2]}  /D = {answer[3]}"
            self.display_queue.put(bytes("TA/"+answers_text,encoding='utf8'))
            dispatcher.utter_message(text=answers_text)
            self.last_activity = "trivia"
        


        elif intent == "nasa" :
            self.display_queue.put(b"nasa")
            image = self.nasaAPI.get_image()
            print("action.py => NASA")
            display_image = "image_nasa "+image
            self.display_queue.put(bytes(display_image, encoding='utf8'))
            txt = self.nasaAPI.get_description()
            dispatcher.utter_message(text = txt)
            self.last_activity = "nasa"

        elif intent == "answer" :
            if self.last_activity == "geo" : 
                entity = tracker.latest_message['entities'][0]['value']
                response = self.geoAPI.check_answer(entity)
                dispatcher.utter_message(text=response)

            elif self.last_activity == "trivia":
                entity = tracker.latest_message['entities'][0]['value']
                response = self.triviaAPI.get_result(entity)

                if response[0] :
                    dispatcher.utter_message(text=f"Bravo, réponse {entity} correct")
                else :
                    dispatcher.utter_message(text=f"Raté,  réponse {entity} incorrecte")
                
                if self.nb_question < 5 :
                    self.nb_question +=1
                    self.display_queue.put(b"trivia")
                    question = self.triviaAPI.get_question()
                    dispatcher.utter_message(text=question)
                    self.display_queue.put(bytes("TQ/"+question,encoding='utf8'))
                    
                    answer = self.triviaAPI.get_choices()
                    answers_text = f"A = {answer[0]}  /B = {answer[1]}  /C = {answer[2]}  /D = {answer[3]}"
                    self.display_queue.put(bytes("TA/"+answers_text,encoding='utf8'))
                    dispatcher.utter_message(text=answers_text)
                    self.last_activity = "trivia"
                else :
                    self.nb_question = 0
            else :
                print("erreur")

        elif intent == "stop_game" :
            self.nb_question = 0
            pass
        
        elif intent == "repeat_question":
            if self.last_activity == "geo" : 
                question = self.geoAPI.current_question
                dispatcher.utter_message(text=question)
            elif self.last_activity == "trivia":
                question = self.triviaAPI.get_question()
                dispatcher.utter_message(text=question)
            else :
                print("erreur")

        
        else:
            dispatcher.utter_message(text=f"Debug : custom action from intent={intent}")
        

        return []

