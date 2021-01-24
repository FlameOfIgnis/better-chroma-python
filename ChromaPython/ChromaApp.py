import requests
from .ChromaBinary import ChromaBcaHandler
from .ChromaDevices import Keyboard, Mouse, Mousepad, ChromaLink, Headset
from .ChromaDatatypes import Heartbeat, ChromaAppInfo
import allogate as logging
import time
class ChromaApp:
    def __init__(self, Info: ChromaAppInfo):
        try:
            self.url = 'http://localhost:54235/razer/chromasdk'

            self.data = {
                "title": Info.Title,
                "description": Info.Description,
                "author": {
                    "name": Info.DeveloperName,
                    "contact": Info.DeveloperContact
                },
                "device_supported": Info.SupportedDevices,
                "category": Info.Category
            }

            #wait for session to fully initialize
            self.await_session()

            logging.pprint(f"URI: {self.URI}", 5)
            logging.pprint("Initializing heartbeat", 4)
            self.heartbeat = Heartbeat(self.URI)
            logging.pprint("Initializing keyboard", 4)
            self.Keyboard = Keyboard(self.URI)
            logging.pprint("Initializing mouse", 4)
            self.Mouse = Mouse(self.URI)
            logging.pprint("Initializing mousepad", 4)
            self.Mousepad = Mousepad(self.URI)
            logging.pprint("Initializing headset", 4)
            self.Headset = Headset(self.URI)
            logging.pprint("Initializing chromalink", 4)
            self.ChromaLink = ChromaLink(self.URI)
            logging.pprint("Initializing chromaBcaHandler", 4)
            self.BcaHandler = ChromaBcaHandler()
        except:
            logging.pprint("ChromaApp Crashed.", 0)
            raise
    
    def negotiate_session(self, data):
        logging.pprint("Sending request to /razer/chromasdk", 4)
        response = requests.post(url=self.url, json=data)
        logging.pprint("Received response from /razer/chromasdk", 4)
        self.SessionID, self.URI = response.json()['sessionid'], response.json()['uri']


    def Version(self):
        try:
            logging.pprint("Getting Version", 4)
            v = requests.get(url='http://localhost:54235/razer/chromasdk').json()['version']
            logging.pprint(f"Chroma SDK Version: {v}", 4)
            return 

        except:
            # TODO Add proper exception handling
            logging.pprint('Unexpected Error!')
            raise

    def __del__(self):
        logging.pprint("Shutting down Chroma App.", 6)
        self.heartbeat.stop()
        requests.delete(self.URI)

    def await_session(self):
        self.negotiate_session(self.data)

        #attempt 3 times at session negotiation and give up if it fails.
        for i in range(3):
            try:
                requests.get(self.URI)
                logging.pprint("Session started", 1)
                time.sleep(0.25)
                return
            except:
                logging.pprint("Timeout reached while waiting for session.")
                return self.await_session()

        logging.pprint("All renegotiations failed. Cannot start chromaApp session.")