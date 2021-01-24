import requests

from .ChromaDatatypes import ChromaColor, checkresult
from .ChromaEnums import KeyboardKeys
from .ChromaBinary import ChromaAnimation
from time import sleep
import allogate as logging

class ChromaDevice():
    def __init__(self, uri:str, maxLED:int=0):
        logging.pprint(f"Initializing {self.__class__.__name__}", 2)
        self._MaxLED = maxLED
        self._ColorGrid = [ChromaColor(red=0, green=0, blue=0) for x in range(self._MaxLED)]

        self.base_URI = uri
        self._URI = ""

    @property
    def MaxLED(self):
        return self._MaxLED

    def setStatic(self, color: ChromaColor):
        try:
            data = {
                "effect": "CHROMA_STATIC",
                "param": {
                    "color": int(color.getHexBGR(), 16)
                }
            }
            return checkresult(requests.put(url=self._URI, json=data).json())
        except:
            # TODO Add proper exception handling
            print('Unexpected Error!')
            raise

    def setNone(self):
        data = {
            "effect": "CHROMA_NONE"
        }
        try:
            return checkresult(requests.put(url=self._URI, json=data).json())
        except:
            # TODO Add proper exception handling
            print('Unexpected Error!')
            raise

    def setCustomGrid(self, grid):
        try:
            for x in range(0, len(self._ColorGrid)):
                self._ColorGrid[x].set(red=grid[x]._red, green=grid[x]._green, blue=grid[x]._blue)
            return True
        except:
            # TODO Add proper exception handling
            print('Unexpected Error!')
            raise

    def applyGrid(self):
        tmp = [0 for x in range(15)]

        for x in range(0, len(self._ColorGrid)):
            tmp[x] = int(self._ColorGrid[x].getHexBGR(), 16)

        data = {
            "effect": "CHROMA_CUSTOM",
            "param": tmp
        }
        try:
            return checkresult(requests.put(url=self._URI, json=data).json())

        except:
            # TODO Add proper exception handling
            print('Unexpected Error!')
            raise

    def setPosition(self, color: ChromaColor, x=0):
        try:

            red, green, blue = color.getRGB()
            self._ColorGrid[x].set(red=red, green=green, blue=blue)

        except:
            # TODO Add proper exception handling
            print('Unexpected Error!')
            raise

class ChromaDevice2D(ChromaDevice):
    def __init__(self, uri: str, row=0, col=0):
        super().__init__(uri)
        self._MaxRow = row
        self._MaxColumn = col
        self._ColorGrid = [[ChromaColor(red=0, green=0, blue=0) for x in range(col)] for y in range(row)]

class Mousepad(ChromaDevice):
    def __init__(self, uri: str):
        super().__init__(uri, maxLED=15)
        self._URI = '/mousepad'

class Headset(ChromaDevice):
    def __init__(self, uri: str):
        super().__init__(uri,  maxLED=2)
        self._URI =  '/headset'

class ChromaLink(ChromaDevice):
    def __init__(self, uri: str):
        super().__init__(uri,  maxLED=5)
        self._URI = '/chromalink'

class Mouse(ChromaDevice2D):
    def __init__(self, uri: str):
        super().__init__(uri, row=9, col=7)
        self._URI = '/mouse'

class Keyboard(ChromaDevice):
    def __init__(self, uri: str):
        super().__init__(uri, row=6, col=22)
        self._URI = uri + '/keyboard'

class Keypad(ChromaDevice):
    def __init__(self, uri: str):
        super().__init__(uri, row=4, col=5)
        self._Keys = KeyboardKeys()
        self._URI = uri + '/keypad'