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
        fullAdress = street + " " + houseNumber
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
            if (finalDistance >= 100000):
                print(f"Vzdálenost nejbližšího kontejneru od adresy {adressesAd} je větší než 10 km.")
                print("!!!Program končí!!!")   
            elif (finalDistance < onGoing):
                onGoing = finalDistance
                print(finalDistance)
        distances[adressesAd] = onGoing
    return distances

#VÝBĚR NEJVZDÁLENĚJŠÍHO KONTEJNERU
def maxDistance(distances):
    maximDistance = max(distances.values())
    for (adress, dis) in distances.items():
        if dis == maximDistance:
            maxstreet = adress
    return maxstreet, maximDistance

def median(distances):
    distancesList = []
    for (_,dis) in distances.items():
        distancesList.append(dis)
    distancesList.sort()
    if ((len(distancesList) % 2) == 0):
        medPositionLower = int((len(distancesList) - 2) / 2)
        medPositionHigher = int((len(distancesList) + 2) / 2)
        medValueLower = distancesList[medPositionLower]
        medValueHigher =  distancesList[medPositionHigher]
        medValue = (medValueLower + medValueHigher) / 2
    elif ((len(distancesList) % 2) == 1):
        medPositionLower = int((len(distancesList) - 1) / 2)
        medPositionHigher = int((len(distancesList) + 1) / 2)
        medValueLower = distancesList[medPositionLower]
        medValueHigher =  distancesList[medPositionHigher]
        medValue = (medValueLower + medValueHigher) / 2
    return medValue


#SAMOTNÝ PRŮBĚH KÓDU
conteiners = "kontejnery1.geojson"
adress = "adresy1.geojson"

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
print(f"Prumerna vzdalenost ke kontejneru je {median(takeDistances)} m.")
print(f"Medián vzdálenosti ke kontejneru je {averageDistance} m.")
print(f"Nejdale ke kontejneru je z adresy {maxstreet[0]} a to {maxstreet[1]} m.\n")