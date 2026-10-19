from pathlib import Path
import pandas as pd

RACINE = Path(__file__).resolve().parent.parent
df = pd.read_parquet(RACINE / "data" / "processed" / "evenements.parquet")

# Les trois colonnes standard d'un journal d'événements
CAS = "case:concept:name"     # identifiant du cas : commande + ligne
ACTIVITE = "concept:name"     # nom de l'étape
DATE = "time:timestamp"       # horodatage de l'étape

print("Événements :", len(df))
print("Cas (lignes de commande) :", df[CAS].nunique())
print("Activités différentes :", df[ACTIVITE].nunique())

print("\nLes 15 activités les plus fréquentes :")
print(df[ACTIVITE].value_counts().head(15))

print("\nPériode couverte :")
print("  première date :", df[DATE].min())
print("  dernière date :", df[DATE].max())

# Le type de rapprochement est une information du cas, répétée sur chaque événement
categorie = [c for c in df.columns if "Item Category" in c][0]
print(f"\nRépartition des cas par type de rapprochement ({categorie}) :")
print(df.drop_duplicates(CAS)[categorie].value_counts())

# Répartition des événements par année
annees = df[DATE].dt.year.value_counts().sort_index()
print("\nÉvénements par année :")
print(annees)

# Cas touchés par une date hors de la fenêtre 2017-2019
hors_periode = (df[DATE].dt.year < 2017) | (df[DATE].dt.year > 2019)
cas_touches = df.loc[hors_periode, CAS].nunique()
print(f"\nÉvénements hors 2017-2019 : {hors_periode.sum()}")
print(f"Cas touchés : {cas_touches} ({cas_touches / df[CAS].nunique():.2%})")