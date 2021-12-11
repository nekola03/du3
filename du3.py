from pyproj import Transformer, CRS
import json
from math import sqrt

#FUNKCE PRO NAČTENÍ GEOJSONU
def loadGeoJson(inputJSON):
    try:
        with open(inputJSON,encoding="UTF-8") as openedJSON:
            file = json.load(openedJSON) ["features"]
            return file
    except FileNotFoundError:
        print(f"Soubor {inputJSON} nebyl nalezen!!")
    except RuntimeError:
        pass
    except ValueError:
        print(f"Soubor {inputJSON} obsahuje chybné hodnoty")
    except PermissionError:
        print(f"Přístup k souboru {inputJSON} byl zamítnut")

#VÝBĚR A ÚPRAVA ATRIBUTŮ V SOUBORU S ADRESAMI
def getDataAdress(inputAdress):
    adress = {}
    for feature in inputAdress:
        street = feature["properties"]["addr:street"]
        houseNumber = feature["properties"]["addr:housenumber"]
        fullAdress = street + "" + houseNumber
        wgs = feature["geometry"]["coordinates"]
        jtsk = wgs2jtsk.transform(wgs[0],wgs[1])
        adress[fullAdress] = jtsk
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
    for (adressesAd, coordinatesAd) in adress.items():
        onGoing = 10000
        for (_,coordinatesCo) in conteiners.items():
            finalDistance = distanceFigure(coordinatesAd, coordinatesCo)
            #repair
            onGoing = finalDistance
        distances[adressesAd] = onGoing
    return distances

def maxDistance(distances):
    maximDistance = max(distances.values())
    for (adress, dis) in distances.items():
        if dis == maximDistance:
            maxstreet = adress
    return maxstreet, maximDistance


#SAMOTNÝ PRŮBĚH KÓDU
conteiners = "kontejnery.geojson"
adress = "adresy.geojson"

conteiners = loadGeoJson(conteiners)
adress = loadGeoJson(adress)
wgs2jtsk = Transformer.from_crs(CRS.from_epsg(4326), CRS.from_epsg(5514), always_xy=True)
generalizeAdress = getDataAdress(adress)
generalizeConteiners = getDataConteiners(conteiners)

takeDistances = distance(generalizeAdress,generalizeConteiners)
averageDistance = sum(takeDistances.values()) / len(takeDistances)

maxstreet = maxDistance(takeDistances)

print(f"Nacteno {len(generalizeAdress)} adresnich bodu.")
print(f"Nacteno {len(generalizeConteiners)} kontejneru na trideny odpad.\n")
print(f"Prumerna vzdalenost ke kontejneru je {averageDistance} m.")
print(f"Nejdale ke kontejneru je z adresy {maxstreet[0]} a to {maxstreet[1]} m.\n")