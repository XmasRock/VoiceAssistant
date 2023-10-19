import sys
import json
import threading
import tkinter as tk
import speech_recognition as sr
import pyttsx3 as tts
from neuralintents import BasicAssistant
from action.SearchInternet import SearchInternet
from action.HorairesTrain import HorairesTrain

# ====================
# --- Class MonAssistant     
# ====================
class MonAssistant:

    # ------------
    # --- init     
    # ------------
    def __init__(self) -> None:
        #self.filename = "MonAssistantDictionary.json"
        #self.dictionary = self.initDictionary()
        self.name = "Annie"
        self.language = "fr-FR"
        #self.listeningColor = self.getFromDictionary("listeningColor")
        self.listeningColor = "red"
        self.notListeningColor = "blue"
        self.say = ""
        self.source = None
        self.activateSayHello = "Salut je suis "+ self.name + " ton assistante et je suis d'humeur à t'aider. HA! HA! Pose moi des questions."
        self.shutdownKeywords = "au revoir"
        self.shutdownSayGoodbye = "bon salut, je vais me coucher"

        #--- init actions
        self.actionSearch = SearchInternet(self)
        self.actionHorairesTrain = HorairesTrain(self)

        self.assistant = BasicAssistant("MonAssistantIntents.json",method_mappings={
            "search": self.actionSearch.process,
            "horairesTrain": self.actionHorairesTrain.process
        })
        self.r = sr.Recognizer()
        self.speaker = tts.init()
        self.speaker.setProperty("rate",150)

        self.assistant.fit_model(epochs=50)
        self.assistant.save_model()

        self.root = tk.Tk()
        self.label = tk.Label(text=self.name, font=("Roboto",120,"bold"))
        self.label.config(fg=self.notListeningColor)
        self.label.pack()


    def initDictionary(self):
        f = open(self.filename)
        dictionary = json.load(f)
        f.close()
        return dictionary

    def getFromDictionary(self, key):
        result = self.dictionary[key]
        result = result.replace("@botName", self.name)
        return result


    # ------------
    # --- testActivation
    # ------------
    def testActivation(self, text):
        result=False

        if "ma chérie" in text or "cocotte" in text:
            result = True
            self.label = tk.Label(text=text, font=("Roboto",120,"bold"))
            self.say = "Oui mon chéri ? Je t'écoute."
            self.speaker.setProperty("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_frFR_JulieM")
        elif self.name.lower() in text:
            result = True
            self.label = tk.Label(text=text, font=("Roboto",120,"bold"))
            self.say = "Oui ? Je t'écoute."
            self.speaker.setProperty("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_frFR_PaulM")
        elif "mon chéri" in text:
            self.label = tk.Label(text=text, font=("Roboto",120,"bold"))
            result = True
            self.say = "Oui ma chérie ? Dis moi."
            self.speaker.setProperty("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_frFR_PaulM")
        elif "poulet" in text or "coco" in text:
            result = True
            self.label = tk.Label(text=text, font=("Roboto",120,"bold"))
            self.say = "Oui mon poulet ? Dis moi."
            self.speaker.setProperty("voice", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_frFR_PaulM")

        return result

    # ------------
    # --- run_assistant
    # ------------
    def run_assistant(self):
        self.prPurple("Démarrage...")
        done = False
        self.tell(self.activateSayHello)
        while not done:
            try:
                with sr.Microphone() as self.source:
                    #self.source = source
                    print("Listen ...")
                    self.r.adjust_for_ambient_noise(self.source, duration=0.2)
                    text = self.listen()
                    print(text)
                    if self.testActivation(text) == True:
                        self.prRed("Activation...")
                        self.tell(self.say)
                        self.label.config(fg=self.listeningColor)
                        text = self.listen()
                        self.prRed(text)
                        if text == self.shutdownKeywords:
                            self.prRed("Shuting down...")
                            self.label.config(fg=self.listeningColor)
                            self.tell(self.shutdownSayGoodbye)
                            self.speaker.stop()
                            # self.root.destroy()
                            self.root.quit()
                            done = True
                            sys.exit(0)
                        else:
                            self.label.config(fg=self.notListeningColor)
                            if text is not None:
                                response = self.assistant.process_input(text)
                                self.prRed("   >>> "+ response)
                                if response is not None:
                                    self.tell(response)
            except Exception as error:
                print(">>>> MonAssistant error: ", error)
                self.label.config(fg=self.notListeningColor)
                continue


    # ------------
    # --- tell
    # ------------
    def tell(self,text):
        self.speaker.say(text)
        self.speaker.runAndWait()

    # ------------
    # --- listen
    # ------------
    def listen(self):
        audio = self.r.listen(self.source)
        text = self.r.recognize_google(audio, language=self.language)
        text = text.lower()
        return text

    def prRed(self,text):
        print("\033[91m {}\033[00m" .format(text))

    def prGreen(self,text): 
        print("\033[92m {}\033[00m" .format(text))

    def prPurple(self,text): 
        print("\033[95m {}\033[00m" .format(text))

    # ------------
    # --- start
    # ------------
    def start(self):
        threading.Thread(target=self.run_assistant).start()
        self.root.mainloop()

    # ------------
    # --- test voices
    # ------------
    def testVoices(self):
        voices = self.speaker.getProperty('voices')
        for voice in voices:
            print(" VOIX:"+ str(voice.id))
            self.speaker.setProperty('voice', voice.id)
            self.tell('Salut poulet.')

# =================================================================
# ===                          RUN MonAssistant                         ===    
# =================================================================
assistant = MonAssistant()
assistant.start()
#assistant.testVoices()
