from pyproj import Transformer, CRS
import json
from math import sqrt


wgs2jtsk = Transformer.from_crs(CRS.from_epsg(4326), CRS.from_epsg(5514), always_xy=True)

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

def getDataAdress(inputAdress):
    adress = {}
    for feature in inputAdress:
        street = feature["properties"]["addr:street"]
        houseNumber = feature["properties"]["addr:housenumber"]
        fullAdress = street + "" + houseNumber
        wgsLat = feature["geometry"]["coordinates"][1]
        wgsLon = feature["geometry"]["coordinates"][0]
        adress[fullAdress] = wgs2jtsk.transform(wgsLat,wgsLon)
    return adress

def getDataConteiners(inputConteners):
    conteiners = {}
    for feature in inputConteners:
        fullAdress = feature["properties"]["STATIONNAME"]
        wgs = feature["geometry"]["coordinates"]
        if feature["properties"]["PRISTUP"] == "volně":
            conteiners[fullAdress] = wgs
    return conteiners

def distanceFigure(x,y):
    distance = sqrt(((x[0] - y[0])**2) + ((x[1] - y[1])**2))
    return distance

def distance(adress, conteiners):
    for (adress_street, adress_coor) in adress:
        for (conteiners_street, conteinters_coor) in conteiners:
            finalDistance = distanceFigure(adress_coor, conteinters_coor)
            if finalDistance > 10000:
                print("Maximální vzdálenost mezi kontejnery")
            else:
                




conteiners = "kontejnery.geojson"
adress = "adresy.geojson"

conteiners = loadGeoJson(conteiners)
adress = loadGeoJson(adress)

generalizeAdress = getDataAdress(adress)
generalizeConteiners = getDataConteiners(conteiners)