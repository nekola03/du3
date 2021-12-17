# du3

# Vysvětlení funkčnosti programu

## Předání parametru
Při spuštění programu a předání parametrů -k či -a s názvy souboru má možnost uživatel určit vlastní GEOJSON soubory. Pokud uživatel nepředá název souboru, program využije předem definované názvy. 

## Funkce pro načtení GeoJsonu
V první části programu je vytvořena funkce loadJSON, která je určena pro načítání dat s kontejnery a adresami. Vstup je testován výjimky související s nenalezením souboru, chybnými hodnotamia zamítnutým přístupem. Pro využití programu by měl každý ze souborů obsahovat atribut adresy (ulice a dovoní číslo) společně se souřadnicemi v systému jtsk či WGS84.

## Výběr a úprava atributů v souboru s adresami
getDataAdress je funkcí, která vybírá a slučuje adresy s domovními čísly ze vstupního souboru. Výstupem jsou adresy jednotlivých staveb společně s jejich lokalizací v systému JTSK uložené ve slovníku. Souřadnice v podobě JTSK jsou získávány pomocí modulu pyproj a funkce transform.

## Výběr a úprava atributů v souboru s kontejnery
Funkce getDataContainers je funkčně obdobou funkce getDataAdress. Program vybírá adresu kontejneru, která v tomto případě nevyžaduje úpravy souřadnice daného kontejneru. Podmínka zajišťuje, že do konečného souboru jsou zapsány pouze ty kontejnery, které jsou volně přístupné.

## Výpočet vzdálenosti od adres k nejbližšímu veřejnému kontejneru
Do funkce s názvem distance vstupují proměnné adresy a kontejnery, které vznikly v rámci předchozích dvou funkcí. Jednotlivé adresní body společně s jejich souřadnicemi vstupují do FOR cyklu, který obsahuje vnořený FOR cyklus s procházením jednotlivých kontejnerů a vybírá nejbližší k dané adrese. Vzdálenost je zjištěna pomocí Pythagorovy věty. Program je ukončen v případě, že nejbližší vzdálenost některého adresního bodu ke kontejneru je větší než 10 km.

## Výběr nejvzdálenějšího kontejneru
Určení nejvzdálenějšího kontejneru ze slovníku s nejbližšími kontejnery je podstatou funkce maxDistance. Po výběru vzdálenosti je pomocí FOR cyklu přiřazena vzdálenost k adresnímu bodu.

## Medián
Výpočet mediánu se opírá o vzestupné seřazení adresních bodů a jejich nejbližších kontejnerů dle vzdálenosti. Následně jsou určeny okolní pozice prostřední hodnoty na základě lichosti či sudosti počtu všech hodnot ze souboru. V poslední části jsou dle pozic vybrány příslušné hodnoty a následně vypočítán medián.

## Samotné využití funkcí
V této části jsou určeny názvy vstupních souborů na základě kterých jsou načteny vstupní soubory. Této funkcionalitě předchází určení kontanty maximální vzdálenosti, ve které se kontejnery budou brát v úvahu. Po úpravě souborů z hlediska adres a souřadnicového systému jsou vybrány vzdálenosti k nejbližšímu veřejnému kontejneru a poté je vypočten průměr. Jetnotlivé výsledky jsou vytisknuty v posledním fragmentu kódu.


