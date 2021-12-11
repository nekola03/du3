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
    adress = {} #vše bude uloženo ve slovníku
    for feature in inputAdress:
        street = feature["properties"]["addr:street"]
        houseNumber = feature["properties"]["addr:housenumber"]
        fullAdress = street + " " + houseNumber #celá adresa do jednoho řetězce
        wgs = feature["geometry"]["coordinates"]
        jtsk = wgs2jtsk.transform(wgs[0],wgs[1]) #transformace dat do jtsk
        adress[fullAdress] = jtsk #přiřazení souřadnic k příslušné adrese
    return adress

#VÝBĚR A ÚPRAVA ATRIBUTŮ V SOUBORU S KONTEJNERY
def getDataConteiners(inputConteners):
    conteiners = {}
    for feature in inputConteners:
        fullAdress = feature["properties"]["STATIONNAME"]
        wgs = feature["geometry"]["coordinates"]
        if feature["properties"]["PRISTUP"] == "volně": # výběr pouze těch kontejnerů, které mají volný přístup
            conteiners[fullAdress] = wgs
    
    return conteiners

#VÝPOČET VZDÁLENOSTI OD ADRES K JEDNOTLIVÝM VEŘEJNÝM KONTEJNERŮM
def distance(adress, conteiners):
    distances = {}
    for (adressesAd, coordinatesAd) in adress.items():
        onGoing = 10000 #proměnná s, která bude přepisována dle 
        for (_,coordinatesCo) in conteiners.items():
            finalDistance = sqrt(((coordinatesAd[0] - coordinatesCo[0])**2) + ((coordinatesAd[1] - coordinatesCo[1])**2)) #výpočet vzdálenosti na základě Pythagovovi věty
            if (finalDistance < onGoing): #neustále se zjišťuje vzdálenost k nejbližšímu kontejneru a přepíše se v proměnné onGoing
                onGoing = finalDistance
        if (onGoing >= 10000): #v případě vzdálenosti ke kontejneru větší než 10 km, program skončí
            print(f"Vzdálenost veřejného kontejneru od adresy {adressesAd} je větší než 10 km.")
            print("!!!Program končí!!!")   
            exit()
        distances[adressesAd] = onGoing #každá asresa se spojí vždy s nejbližší vzdáleností k veřejnému kontejneru
    return distances

#VÝBĚR NEJVZDÁLENĚJŠÍHO KONTEJNERU
def maxDistance(distances):
    maximDistance = max(distances.values()) #získání největší vzdálenosti nejbližšího kontejneru z výběru adres
    for (adress, dis) in distances.items(): #cyklus, který zjistí na základě rovnosti adresu dle proměnné maximDistance
        if dis == maximDistance:
            maxstreet = adress
    return maxstreet, maximDistance

#MEDIÁN
def median(distances):
    distancesList = [] 
    for (_,dis) in distances.items(): #pro snazší práci se vybere ze slovníku pouze vzdálenost a zapíše do pole
        distancesList.append(dis)
    distancesList.sort() #sezaření vzestupně
    if ((len(distancesList) % 2) == 0): #výpočet pozic okolních hodnot mediánu v případě sudého počtu hodnot 
        medPositionLower = int((len(distancesList)) / 2)
        medPositionHigher = int((len(distancesList) + 2) / 2)
    elif ((len(distancesList) % 2) == 1): #výpočet pozic okolních hodnot mediánu v případě lichého počtu hodnot 
        medPositionLower = int((len(distancesList) - 1) / 2)
        medPositionHigher = int((len(distancesList) + 1) / 2)
    medValueLower = distancesList[medPositionLower] #zjištění hodnoty na základě pozicev listu
    medValueHigher =  distancesList[medPositionHigher]
    medValue = (medValueLower + medValueHigher) / 2 #výpočet průměru z okolních hodnot
    return medValue

#SAMOTNÝ PRŮBĚH KÓDU
#názvy vstupních souborů
conteiners = "kontejnery.geojson"
adress = "adresy.geojson"

#načtení vstupních souborů
conteiners = loadGeoJson(conteiners)
adress = loadGeoJson(adress)

wgs2jtsk = Transformer.from_crs(CRS.from_epsg(4326), CRS.from_epsg(5514), always_xy=True) #vytvoření transformeru pro převod

#výběr a následná úprava vstupních dat
generalizeAdress = getDataAdress(adress) 
generalizeConteiners = getDataConteiners(conteiners)


takeDistances = distance(generalizeAdress,generalizeConteiners) #výpočet vzdáleností na základě výše popsané vunkce
averageDistance = sum(takeDistances.values()) / len(takeDistances) #průměr všech nejbližších vzáleností
maxstreet = maxDistance(takeDistances)

#tisk všech výstupů
print(f"Nacteno {len(generalizeAdress)} adresnich bodu.")
print(f"Nacteno {len(generalizeConteiners)} kontejneru na trideny odpad.\n")
print(f"Prumerna vzdalenost ke kontejneru je {median(takeDistances):.0f} m.") #vstup do mediánu z prověné takeDistances
print(f"Medián vzdálenosti ke kontejneru je {averageDistance:.0f} m.")
print(f"Nejdale ke kontejneru je z adresy {maxstreet[0]} a to {maxstreet[1]:.0f} m.\n")