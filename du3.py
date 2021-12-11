from pyproj import transformer
import json

def loadGeoJson(inputJSON):
    try:
        with open(inputJSON,encoding="UTF-8") as openedJSON:
            file = json.load(openedJSON) ["features"]
            return file
    except FileNotFoundError:
        print("Soubor nemohl být načtený z důvodu nevalidníhi vstupního souboru")
    except RuntimeError:
        print("ahoj světe")
    except ValueError:
        print("ahoj světe")
    except PermissionError:
        print("ahoj světe")