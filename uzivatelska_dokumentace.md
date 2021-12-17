# Uživatelská dokumentace

## Vstupní soubory
Program pracuje se dvěma vstupními soubory, přičemž musí obsahovat atribut `features`.

### Vstupní soubor s kontejnery
Vstupní soubor kontejnerů musí obsahovat alespoň lokalizaci kontejneru v systému JTSK. Dále musí být uvedena adresa společně s domovním číslem v rámci jednoho atributu a atribut přístupu ke kontejneru. Atributy musí být uvedeny následujícím způsobem.
```
{
    "features" : [
	{
		"geometry" : {
			"coordinates" : [ -741687.4500369802, -1044981.8600061499 ]
		},
		"properties" : {
			"STATIONNAME" : "Máchova 1137/8",
			"PRISTUP" : "volně"
		}
    },
}
```
Soubor by měl být pojmenován jako `kontejnery.geojson`.

### Vstupní soubor s adresními body
Vstupní soubor adresních bodů musí obsahovat alespoň lokalizaci adresních bodů v systému WGS-84. Dále musí být uvedena adresa a domovní číslo v samostatných atributech. Názvy atributů musí být uvedeny následujícím způsobem.
```
{
"features": [
    {
      "properties": {
        "addr:housenumber": "1090/32",
        "addr:street": "Cíglerova",
      },
      "geometry": {
        "coordinates": [14.5681894, 50.1074645]
      },
    }
}
```
Soubor by měl být pojmenován jako `adresy.geojson`.

### Formát vstupních souborů
Vstupní soubory musí být uloženy ve formátu GeoJSON.

## Parametry příkazové řádky
Pro vstup vlastních souborů otevřete příkazový řádek a program vyvolejte následujícím způsobem: `py du3.py -a <soubor_s_adresami> -k <soubor_s_kontejnery>`. Při vynechází jednoho z parametrů se vyvolá určitý předdefinovaný soubor.

## Výstup
Výstup, resp. výsledek, je zobrazen v terminálu či v příkazovém řádku.
```
Nacteno 609 adresnich bodu.
Nacteno 3430 kontejneru na trideny odpad.

Prumerna vzdalenost ke kontejneru je 12 m.
Medián vzdálenosti ke kontejneru je 13 m.
Nejdale ke kontejneru je z adresy Cíglerova 1090/32 a to 73 m.
```


