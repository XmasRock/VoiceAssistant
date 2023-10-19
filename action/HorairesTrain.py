from duckduckgo_search import DDGS
import requests
from transformers import pipeline

# ====================
# --- Class SearchInternet     
# ====================
class HorairesTrain():

    def __init__(self, assistant) -> None:
        self.assistant = assistant
        self.gareDepart = ""
        self.gareArrivee = ""
        self.jour = ""
        self.heureDepart = ""
        self.heureArrivee = ""


    # ------------
    # --- process     
    # ------------
    def process(self):
        self.assistant.tell("Bien sur. Un train au départ de quel gare ?")
        #text = self.assistant.listen_and_verify()
        self.gareDepart = self.assistant.listen()
        self.assistant.tell("Gare d'arrivée ?")
        self.gareArrivee = self.assistant.listen()
        self.assistant.tell("jour ?")
        self.jour = self.assistant.listen()
        self.assistant.tell("Heure de départ ?")
        self.heureDepart = self.assistant.listen()
        try:
            with DDGS() as ddgs:
                search = (
                    "Horaires de trains au départ de la gare " + self.gareDepart + 
                    " et à l'arrivée à la gare " + self.gareArrivee + 
                    " départ le jour " + self.jour + 
                    " aux environs de " + self.heureDepart 
                )
                print("ce que je cherche ==> " + search)
                results = ddgs.text(search, max_results=1)
                #print(results)
                for res in results:
                    print(" res ==> " + str(res))
                    response = requests.get(res['href'])
                    print(" response ==> " + str(response))
                    #question_answerer = pipeline("question-answering")
                    #result = question_answerer(question="What is a good summary of times", context=res['body'])
                    #print(f"Answer: '{result['answer']}', score: {round(result['score'], 4)}, start: {result['start']}, end: {result['end']}")

                    #self.assistant.tell(r)
        except Exception as error:
            print(" >>> ERROR: ", error)


