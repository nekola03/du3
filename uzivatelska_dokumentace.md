# du3

# Uživatelská dokumentace

## Vstupní soubor kontejnerů
Vstupní soubor kontejnerů musí obsahovat alespoň lokalizaci kontejneru v systému JTSK. Dále musí být uvedena adresa společně s domovním číslem v rámci jednoho atributu.

## Vstupní soubor adresních bodů 
Vstupní soubor kontejnerů musí obsahovat alespoň lokalizaci adresních bodů v systému WGS-84. Dále musí být uvedena adresa a domovní číslo v samostatných atributech

## Formát vstupních souborů
Vstupní soubory musí být uloženy ve formátu GeoJSON.

## Parametry příkazové řádky
Pro vstup vlastních souborů otevřete příkazový řádek a program vyvolejte následujícím způsobem: `py du3.py -a <soubor_s_adresami> -k <soubor_s_kontejnery>`. Při vynechází jednoho z parametrů se vyvolá určitý předdefinovaný soubor.


