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

    @property
    def URI(self):
        return self.base_URI + self._URI

    def setEffect(self, effect:str, param=None):
        logging.pprint(f"Setting {self.__class__.__name__} effect to {effect}", 5)
        logging.pprint(f"Param: {param}", 6)
        try:
            data = {"effect": effect}
            if(param):
                data["param"] = param
            return checkresult(requests.put(url=self.URI, json=data).json())
        except:
            # TODO Add proper exception handling
            logging.pprint('Unexpected Error!')
            raise

    def setStatic(self, color: ChromaColor):
        return self.setEffect(effect="CHROMA_STATIC", param={"color": int(color.getHexBGR(), 16)})

    def setNone(self):
        return self.setEffect(effect="CHROMA_NONE")

    def setCustomGrid(self, grid):
        for x in range(0, self._MaxLED):
            self._ColorGrid[x].set(red=grid[x]._red, green=grid[x]._green, blue=grid[x]._blue)
        return True

    def applyGrid(self):
        buf = [int(self._ColorGrid[x].getHexBGR(), 16) for x in range(self._MaxLED)]
        return self.setEffect(effect="CHROMA_CUSTOM", param=buf)

    def setPosition(self, color: ChromaColor, x=0):
        self._ColorGrid[x].set(*color.getRGB())
        return True

class ChromaDevice2D(ChromaDevice):
    def __init__(self, uri: str, row=0, col=0):
        super().__init__(uri)
        self._MaxRow = row
        self._MaxColumn = col
        self._ColorGrid = [[ChromaColor(red=0, green=0, blue=0) for x in range(col)] for y in range(row)]

    def setCustomGrid(self, grid):
        for i in range(0, len(self._ColorGrid)):
            for j in range(0, len(self._ColorGrid[i])):
                self._ColorGrid[i][j].set(red=grid[i][j]._red, green=grid[i][j]._green, blue=grid[i][j]._blue)
        return True

    def applyGrid(self):
        tmp = [ [0] * self.col] * self.row

        for i in range(0, self.row):
            for j in range(0, self.col):
                tmp[i][j] = int(self._ColorGrid[i][j].getHexBGR(), 16)

        self.setEffect(effect="CHROMA_CUSTOM", param=[tmp[i] for i in range(self.row)])
    
    def setPosition(self, color: ChromaColor, x=0, y=0):
        red, green, blue = color.getRGB()
        self._ColorGrid[y][x].set(red=red, green=green, blue=blue)
        return True

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

class Keyboard(ChromaDevice2D):
    def __init__(self, uri: str):
        super().__init__(uri, row=6, col=22)
        self._URI = uri + '/keyboard'

    def setCustomKey(self, key=None, keys=None):
        try:
            if keys is not None:
                for item in keys:
                    row = int(item._Key, 16) >> 8
                    col = int(item._Key, 16) & 0xFF

                    red, green, blue = item._Color.getRGB()
                    self._ColorGrid[row][col].set(red=red, green=green, blue=blue)

            if key is not None:
                row = int(int(key._Key, 16) >> 8)
                col = int(int(key._Key, 16) & 0xFF)

                red, green, blue = key._Color.getRGB()
                self._ColorGrid[row][col].set(red=red, green=green, blue=blue)
            return True
        except:
            # TODO Add proper exception handling
            logging.pprint('Unexpected Error!')
            raise

    def playAnimation(self, animation: ChromaAnimation):
        for i in range(0, len(animation.Frames)):
            self.setCustomGrid(animation.Frames[i])
            self.applyGrid()
            sleep(1 / animation.FPS)

class Keypad(ChromaDevice):
    def __init__(self, uri: str):
        super().__init__(uri, row=4, col=5)
        self._Keys = KeyboardKeys()
        self._URI = uri + '/keypad'