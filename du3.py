from pyproj import Transformer, CRS
import json
from math import sqrt
import argparse

#názvy vstupních souborů
containers = "kontejnery.geojson"
adress = "adresy.geojson"

#PŘEDÁNÍ PARAMETRŮ
parameters = argparse.ArgumentParser(description='Výpočet vzdálenosti k nejbližšímu kontejneru od jednotlivých adres')
parameters.add_argument('-a', '--adresy', type = str, required = False, help = 'Soubor s adresními body ve formátu GEOJSON. Soubor musí obsahovat atribut adresy, domovního čísla společně s lokalizací v souřadnicovém systému WGS84.')
parameters.add_argument('-k', '--kontejnery', type = str, required = False, help = 'Soubor s kontejnery ve formátu GEOJSON. Soubor musí obsahovat atribut adresy s domovním číslem společně s lokalizací v souřadnicovém systému JTSK.')
args = parameters.parse_args()
if args.adresy is not None: #dvojitý zápor, takže pokud existuje zadaný parametr
    adress = args.adresy 
elif args.kontejnery is not None:
    containers = args.kontejnery

#FUNKCE PRO NAČTENÍ GEOJSONU
def loadGeoJson(inputJSON):
    try:
        with open(inputJSON,encoding="UTF-8") as openedJSON:
            file = json.load(openedJSON) ["features"]
            return file
    except FileNotFoundError:
        print(f"Soubor {inputJSON} nebyl nalezen!!")
    except ValueError:
        print(f"Soubor {inputJSON} obsahuje chybné hodnoty")
    except PermissionError:
        print(f"Přístup k souboru {inputJSON} byl zamítnut")

#VÝBĚR A ÚPRAVA ATRIBUTŮ V SOUBORU S ADRESAMI
def getDataAdress(inputAdress,wgs2jtsk):
    adress = {} #vše bude uloženo ve slovníku
    for feature in inputAdress:
        street = feature["properties"]["addr:street"]
        houseNumber = feature["properties"]["addr:housenumber"]
        fullAdress = street + " " + houseNumber #celá adresa do jednoho řetězce
        wgsCO = feature["geometry"]["coordinates"]
        jtskCO = wgs2jtsk.transform(wgsCO[0],wgsCO[1]) #transformace dat do jtsk
        adress[fullAdress] = jtskCO #přiřazení souřadnic k příslušné adrese
    return adress

#VÝBĚR A ÚPRAVA ATRIBUTŮ V SOUBORU S KONTEJNERY
def getDataContainers(inputContainers):
    containers = {}
    for feature in inputContainers:
        fullAdress = feature["properties"]["STATIONNAME"]
        jtskCO = feature["geometry"]["coordinates"]
        if feature["properties"]["PRISTUP"] == "volně": # výběr pouze těch kontejnerů, které mají volný přístup
            containers[fullAdress] = jtskCO
    return containers

#VÝPOČET VZDÁLENOSTI OD ADRES K NEJBLIŽŠÍMU VEŘEJNÉMU KONTEJNERU
def distance(adress, containers, PERMISSIBLE_DIS):
    distances = {}
    for (adressesAd, coordinatesAd) in adress.items():
        for coordinatesCo in containers.values():
            finalDistance = sqrt(((coordinatesAd[0] - coordinatesCo[0])**2) + ((coordinatesAd[1] - coordinatesCo[1])**2)) #výpočet vzdálenosti na základě Pythagovovi věty
            if (finalDistance < PERMISSIBLE_DIS): #neustále se zjišťuje vzdálenost k nejbližšímu kontejneru a přepíše se v proměnné PERMISSIBLE_DIS
                PERMISSIBLE_DIS = finalDistance
        if (PERMISSIBLE_DIS >= 10000): #v případě vzdálenosti ke kontejneru větší než 10 km, program skončí
            print(f"Vzdálenost veřejného kontejneru od adresy {adressesAd} je větší než 10 km.")
            print("!!!Program končí!!!")   
            exit()
        distances[adressesAd] = PERMISSIBLE_DIS #každá asresa se spojí vždy s nejbližší vzdáleností k veřejnému kontejneru
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
    """
    distancesList = [] 
    for (_,dis) in distances.items(): #pro snazší práci se vybere ze slovníku pouze vzdálenost a zapíše do pole
        distancesList.append(dis)
    distancesList.sort() #sezaření vzestupně
    """
    distancesList = sorted(list(distances.values()))
    if ((len(distancesList) % 2) == 0): #výpočet pozic okolních hodnot mediánu v případě sudého počtu hodnot 
        medPositionLower = (len(distancesList)) // 2
        medPositionHigher = (len(distancesList) + 2) // 2
    elif ((len(distancesList) % 2) == 1): #výpočet pozic okolních hodnot mediánu v případě lichého počtu hodnot 
        medPositionLower = (len(distancesList) - 1) // 2
        medPositionHigher = (len(distancesList) + 1) // 2
    medValueLower = distancesList[medPositionLower] #zjištění hodnoty na základě pozicev listu
    medValueHigher =  distancesList[medPositionHigher]
    medValue = (medValueLower + medValueHigher) / 2 #výpočet průměru z okolních hodnot
    return medValue

#SAMOTNÉ VYUŽITÍ FUNKCÍ
PERMISSIBLE_DIS = 10000 #maximální vzdálenost kontejnerů braných v úvahu

#načtení vstupních souborů
containers = loadGeoJson(containers)
adress = loadGeoJson(adress)

wgs2jtsk = Transformer.from_crs(CRS.from_epsg(4326), CRS.from_epsg(5514), always_xy=True) #vytvoření transformeru pro převod

#výběr a následná úprava vstupních dat
generalizeAdress = getDataAdress(adress,wgs2jtsk) 
generalizeContainers = getDataContainers(containers)


takeDistances = distance(generalizeAdress,generalizeContainers, PERMISSIBLE_DIS) #výpočet vzdáleností na základě výše popsané vunkce
averageDistance = sum(takeDistances.values()) / len(takeDistances) #průměr všech nejbližších vzáleností
maxstreet = maxDistance(takeDistances)

#tisk všech výstupů
print(f"Nacteno {len(generalizeAdress)} adresnich bodu.")
print(f"Nacteno {len(generalizeContainers)} kontejneru na trideny odpad.\n")
print(f"Prumerna vzdalenost ke kontejneru je {median(takeDistances):.0f} m.") #vstup do mediánu z prověné takeDistances
print(f"Medián vzdálenosti ke kontejneru je {averageDistance:.0f} m.")
print(f"Nejdale ke kontejneru je z adresy {maxstreet[0]} a to {maxstreet[1]:.0f} m.\n")