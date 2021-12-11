from pyproj import Transformer, CRS
import json
from math import sqrt


wgs2jtsk = Transformer.from_crs(CRS.from_epsg(4326), CRS.from_epsg(5514), always_xy=True)

#FUNKCE PRO NAČTENÍ GEOJSONU
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

#VÝBĚR A ÚPRAVA ATRIBUTŮ V SOUBORU S ADRESAMI
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

#VÝBĚR A ÚPRAVA ATRIBUTŮ V SOUBORU S KONTEJNERY
def getDataConteiners(inputConteners):
    conteiners = {}
    for feature in inputConteners:
        fullAdress = feature["properties"]["STATIONNAME"]
        wgs = feature["geometry"]["coordinates"]
        if feature["properties"]["PRISTUP"] == "volně":
            conteiners[fullAdress] = wgs
    return conteiners

#VZOREC PRO VÝPOČET VZDÁLENOSTI
def distanceFigure(x,y):
    distance = sqrt(((x[0] - y[0])**2) + ((x[1] - y[1])**2))
    return distance

#VÝPOČET VZDÁLENOSTI OD ADRES K JEDNOTLIVÝM VEŘEJNÝM KONTEJNERŮM
def distance(adress, conteiners):
    distances = {}
    for (adress_street, adress_coor) in adress:
        onGoing = 10000
        for (conteinters_coor) in conteiners:
            finalDistance = distanceFigure(adress_coor, conteinters_coor)
            if finalDistance > 10000:
                print("Maximální vzdálenost mezi kontejnery")
                exit()
            elif finalDistance <= onGoing:
                onGoing = finalDistance
        distances[adress_street] = onGoing
    return distances

#SAMOTNÝ PRŮBĚH KÓDU
conteiners = "kontejnery.geojson"
adress = "adresy.geojson"

conteiners = loadGeoJson(conteiners)
adress = loadGeoJson(adress)

generalizeAdress = getDataAdress(adress)
generalizeConteiners = getDataConteiners(conteiners)