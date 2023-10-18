from duckduckgo_search import DDGS

# ====================
# --- Class SearchInternet     
# ====================
#class SearchInternet(ActionGeneric):
class SearchInternet():

    def __init__(self, assistant) -> None:
        self.assistant = assistant


    # ------------
    # --- process     
    # ------------
    def process(self):
        self.assistant.tell("Dis moi ce que tu cherches ?")
        text = self.assistant.listen()
        if text is not None:
            with DDGS() as ddgs:
                print("ce que je cherche ==> " + text)
                #results = ddgs.answers(text)
                results = [r for r in ddgs.text(text, max_results=3)]
                #print(results)
                for res in results:
                    print(res)
                    #self.assistant.tell(r)


