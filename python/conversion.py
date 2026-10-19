from pathlib import Path
import pm4py

RACINE = Path(__file__).resolve().parent.parent
SOURCE = RACINE / "data" / "raw" / "BPI_Challenge_2019.xes"
SORTIE = RACINE / "data" / "processed" / "evenements.parquet"

# Lecture du journal XES : PM4Py renvoie directement une table Pandas
journal = pm4py.read_xes(str(SOURCE))

print("Lignes, colonnes :", journal.shape)
print("\nColonnes :")
for colonne in journal.columns:
    print(" -", colonne)

SORTIE.parent.mkdir(parents=True, exist_ok=True)
journal.to_parquet(SORTIE, index=False)
print("\nFichier écrit :", SORTIE)