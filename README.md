# Programska koda eksperimenta pri diplomskem  delu

V tem repozitoriju je zbrana vsa programska koda, ki je bila razvita za analizo, predpripravo podatkov in izvedbo algoritmov nenegativne matrične faktorizacije (NMF) in metode glavnih komponent (PCA).


## Struktura map

### ```najbolj_popularne```
Vsebuje kodo za analizo najbolj popularnih knjig kadarkoli (vir: Goodreads Best Books Ever). Koda vlkjučuje:
- predprocesiranje podatkov in gradnjo podatkovne matrike,
- implementacijo algoritma NMF,
- analizo z NMf in določitev tematik,
- analizo s PCA in določitev glavnih komponent.

### ```leto_2003```
Vsebuje kodo za analizo knjig, ki so bile izdane leta 2003 (vir: Goodreads Books Published in 2003). Koda vključuje:
- predprocesiranje podatkov in gradnjo podatkovne matrike,
- implementacijo algoritma NMF,
- analizo z NMf in določitev tematik,
- analizo s PCA in določitev glavnih komponent.

## Programski jezik in knjižnice
Koda je napisana v jeziku ```Python```, najbolj uporabljene knjižnice pa so:
- ```numpy```,
- ```pandas```,
- ```scikit-learn```,
- ```matplotlib```.
