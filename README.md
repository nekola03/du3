# du3

VYSVĚTLENÍ FUNKČNOSTI PROGRAMU

FUNKCE PRO NAČTENÍ GEOJSONU
V první části programu je vytvořena funkce loadJSON, která je určena pro načítání dat s kontejnery a adresami. Vstup je testován na 4 různé výjimky.

VÝBĚR A ÚPRAVA ATRIBUTŮ V SOUBORU S ADRESAMI
getDataAdress je funkcí, která vybere a sloučí adresy s domovními čísly ze vstupního souboru. Výstupem jsou adresy jednotlivých staveb společně s jejich lokalizací v systému JTSK uložené ve slovníku. Souřadnice v podobě JTSK byly získány pomocí modulu pyproj a funkce transform.

VÝBĚR A ÚPRAVA ATRIBUTŮ V SOUBORU S KONTEJNERY
Funkce getDataConteiners je funkčně obdobou funkce getDataAdress. Program vybere adresu kontejneru, která v tomto případě nevyžaduje úpravy souřadnice daného kontejneru. Podmínka zajišťuje, že do konečného souboru budou zapsány pouze ty kontejnery, které jsou volně přístupné.

VÝPOČET VZDÁLENOSTI OD ADRES K NEJBLIŽŠÍMU VEŘEJNÉMU KONTEJNERU
Do funkce s názvem distance vstupují proměnné adresy a kontejnery, které vznikly v rámci předchozích dvou funkcí. Jednotlivé adresní body společně s jejich souřadnicemi vstupují do FOR cyklu, který obsahuje vnořený FOR cyklus s procházením jednotlivých kontejnerů a vybírá nejbližší k dané adrese. Vzdálenost je zjištěna pomocí Pythagorovi věty. Na konci programu je umožňen jeho konec v případě, že nejbližší vzdálenost některého adresního bodu ke kontejneru je větší než 10 km.

VÝBĚR NEJVZDÁLENĚJŠÍHO KONTEJNERU
Určení nejvzdálenějšího kontejneru ze slovníku s nejbližšími kontejnery je podtatou funkce maxDistance. Po výběru vzdálenosti je pomocí FOR cyklu přiřazena vzdálenost k adresnímu bodu.

MEDIÁN
Výpočet mediánu se opírá o vzestupné seřazení adresních bodů a jejich nejbližších kontejnerů dle vzdálenosti. Následně jsou určeny okolní pozice prostřední hodnoty na základě lichosti či sudosti počtu všech hodnot ze souboru. V poslední části jsou dle pozic vybrány příslušné hodnoty a následně vypočítán medián.

SAMOTNÉ VYUŽITÍ FUNKCÍ
V této části jsou určeny názvy vstupních souborů na základě kterých budou načteny vstupní soubory. Po úpravě souborů z hlediska adres a souřadnicového systému budou vybrány vzdálenosti k nejbližšímu veřejnému kontejneru a poté vypočten průměr. Jetnotlivé výsledky jsou vytisknuty v posledním fragmentu kódu.


