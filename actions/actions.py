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
        self.current_player = ""
        self.compteur_incompris = 0

    def name(self) -> Text:
        return "action_API"

    def question_Trivia(self, dispatcher : CollectingDispatcher, regenerate = False , update_display = True, reset_score = False) :
        if reset_score :
            self.nb_question = 1
            self.current_score = 0
        self.last_activity = "trivia"

        if regenerate :
            self.triviaAPI.generate_question()

        question = self.triviaAPI.get_question()
        dispatcher.utter_message(text=question)
        
        answers = self.triviaAPI.get_choices()
        dispatcher.utter_message(text=f"A = {answers[0]}")
        dispatcher.utter_message(text=f"B = {answers[1]}")
        dispatcher.utter_message(text=f"C = {answers[2]}")
        dispatcher.utter_message(text=f"D = {answers[3]}")
        
        if update_display :
            answers_text = f"A = {answers[0]}  /B = {answers[1]}  /C = {answers[2]}  /D = {answers[3]}"
            self.display_queue.put(b"trivia")
            self.display_queue.put(bytes("TQ/"+question,encoding='utf8'))
            self.display_queue.put(bytes("TA/"+answers_text,encoding='utf8'))

    def question_Geo(self, dispatcher : CollectingDispatcher, regenerate = False , update_display = True, debug = False):
        self.last_activity = "geo"

        if regenerate :
            type, question = self.geoAPI.get_question()
        else :
            type = self.geoAPI.current_data_type
            question = self.geoAPI.current_question

        if type == "flag":
            dispatcher.utter_message(text=question, image=FLAG_IMG_PATH)
        else:
            dispatcher.utter_message(text=question)

        answers = self.geoAPI.get_choices()
        dispatcher.utter_message(text=f"{answers[0]}")
        dispatcher.utter_message(text=f"{answers[1]}")
        dispatcher.utter_message(text=f"{answers[2]}")
        dispatcher.utter_message(text=f"{answers[3]}")
        
        if update_display :
            answers_text = f"{answers[0]} /{answers[1]} /{answers[2]} /{answers[3]}"
            self.display_queue.put(b"geography")
            if type == "flag":
                self.display_queue.put(bytes("GF/T",encoding='utf8'))
            else:
                self.display_queue.put(bytes("GF/F",encoding='utf8'))
            self.display_queue.put(bytes("GQ/"+question,encoding='utf8'))
            self.display_queue.put(bytes("GA/"+answers_text,encoding='utf8'))

        if debug :
            print(f"type={type}, question={question}")

    def action_nasa(self,dispatcher):
        self.display_queue.put(b"nasa")

        image = self.nasaAPI.get_image()
        display_image = "image_nasa "+image
        self.display_queue.put(bytes(display_image, encoding='utf8'))

        txt = self.nasaAPI.get_description()
        dispatcher.utter_message(text = txt)
        self.last_activity = "nasa"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message['intent'].get('name')

        print(f"\nintent = {intent}\n")
        if intent in ["geography","trivia","nasa","answer","stop_game","repeat_question","play_again"] :
            self.compteur_incompris = 0

        if intent == "geography" :
            self.question_Geo(dispatcher,regenerate=True,update_display=True,debug=True)

        elif intent == "trivia" :
            self.question_Trivia(dispatcher,regenerate=True,update_display=True,reset_score=True)

        elif intent == "nasa" :
            self.action_nasa(dispatcher)

        elif intent == "answer" :
            if self.last_activity == "geo" : 
                entity = tracker.latest_message['entities'][0]['value']
                response = self.geoAPI.check_answer(entity)
                dispatcher.utter_message(text=response)
                self.display_queue.put(b'IDLE')

            elif self.last_activity == "trivia":
                entity = tracker.latest_message['entities'][0]['value']
                response = self.triviaAPI.get_result(entity)

                dispatcher.utter_message(text=response[2]) # donner la réponse à l'user
                if response[0] : # si réponse correcte
                    self.current_score += response[1]

                if self.nb_question < 5 : # enchainement des 5 questions
                    self.nb_question +=1
                    self.question_Trivia(dispatcher,regenerate=True,update_display=True,reset_score=False)
                else :
                    self.nb_question = 0
                    dispatcher.utter_message(text=f"Well done, you achieved a score of {self.current_score} !")
                    self.display_queue.put(b"scoreboard_trivia")
                    self.display_queue.put(bytes(f"score {self.current_score}",encoding='utf8'))
            else :
                dispatcher.utter_message(text=f"I understood that you wanted to answer a question but i havn't asked any, you can start an activity by saying 'I want to play trivia'")

        elif intent == "stop_game" :
            self.nb_question = 0
            self.current_score = 0
            pass
        
        elif intent == "repeat_question":
            if self.last_activity == "geo" :
                self.question_Geo(dispatcher,regenerate=False,update_display=False)

            elif self.last_activity == "trivia":
                self.question_Trivia(dispatcher,regenerate=False,update_display=False,reset_score=False)
            else :
                dispatcher.utter_message(text="Sorry, I am not sure what question you want me to repeat.")

        
        elif intent == "play_again":
            if self.last_activity == "geo" : 
                self.question_Geo(dispatcher, regenerate=True,update_display=True)

            elif self.last_activity == "trivia":
                self.question_Trivia(dispatcher,regenerate=True,update_display=True,reset_score=True)
            else :
                dispatcher.utter_message(text=f"Maybe we should initiate a game today before trying to play again.")
        else:
            if self.compteur_incompris < 2 :
                dispatcher.utter_message(text=f"I did not understood what you just said, may you repeat ?")
                self.compteur_incompris += 1
            elif self.compteur_incompris < 3:
                dispatcher.utter_message(text=f"If you ever need help just say help or help followed by the activity you need more information about")
        

        return []

