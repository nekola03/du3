# du3

VYSVĚTLENÍ FUNKČNOSTI PROGRAMU

FUNKCE PRO NAČTENÍ GEOJSONU
V první části programu je vytvořena funkce loadJSON, která určena pro načítání dat s kontejnery a adresami. Vstup je testován na 4 různé výjimky

VÝBĚR A ÚPRAVA ATRIBUTŮ V SOUBORU S ADRESAMI
getDataAdress je funkcí, která vybere a sloučí adresy s domovními čísly ze vstupního souboru. Výstupem jsou adresy jednotlivých staveb společně s jejich lokalizací v systému JTSK. Souřadnice v podobě JTSK byly získány pomocí modulu pyproj a funkce transform. Výstup je uložen v knihovně. 

VÝBĚR A ÚPRAVA ATRIBUTŮ V SOUBORU S KONTEJNERY
Funkce getDataConteiners je funkčně obdobou funkce getDataAdress. Program vybere adresu kontejneru, která se v tomto případě nemusí upravovat stejně jako souřadnice daného kontejneru. Podmínka zajišťuje, že do konečného souboru budou zapsány pouze ty kontejnery, které jsou volně přístupné.

