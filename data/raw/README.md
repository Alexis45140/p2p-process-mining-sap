# Données brutes

Le fichier source n'est pas versionné (environ 695 Mo).

1. Télécharger le jeu **BPI Challenge 2019** sur 4TU.ResearchData :
   https://doi.org/10.4121/uuid:d06aff4b-79f0-45e6-8ec8-e19730c248f1
2. Placer le fichier, sans le renommer, à cet emplacement :

   ```
   data/raw/BPI_Challenge_2019.xes
   ```

   Taille attendue : 728 558 522 octets.

3. Lancer la conversion depuis la racine du dépôt :

   ```
   python python/conversion.py
   ```

   Elle écrit `data/processed/evenements.parquet`, lu ensuite par dbt.

Licence : CC BY 4.0.
Citation : van Dongen, Boudewijn (2019). BPI Challenge 2019. 4TU.ResearchData. Dataset.
https://doi.org/10.4121/uuid:d06aff4b-79f0-45e6-8ec8-e19730c248f1
