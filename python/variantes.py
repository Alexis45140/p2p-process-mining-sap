from pathlib import Path
import duckdb

RACINE = Path(__file__).resolve().parent.parent
con = duckdb.connect(str(RACINE / "data" / "p2p.duckdb"), read_only=True)

df = con.sql("""
    select cas_id, activite, horodatage, type_rapprochement
    from int_evenements_valides
""").df()

# Remettre les étapes de chaque cas dans l'ordre chronologique
df = df.sort_values(["cas_id", "horodatage"], kind="stable")

# Construire la variante de chaque cas : la suite de ses étapes
variantes = (
    df.groupby("cas_id")
    .agg(
        variante=("activite", " → ".join),
        type_rapprochement=("type_rapprochement", "first"),
    )
)

nb_cas = len(variantes)
comptage = variantes["variante"].value_counts()

print(f"Cas : {nb_cas:,}")
print(f"Variantes différentes : {len(comptage):,}")

top10 = comptage.head(10)
print(f"\nPart des cas couverts par les 10 variantes les plus fréquentes : "
      f"{top10.sum() / nb_cas:.1%}")

print("\nLes 10 variantes les plus fréquentes :")
for rang, (variante, nb) in enumerate(top10.items(), start=1):
    print(f"\n{rang}. {nb:,} cas ({nb / nb_cas:.1%})")
    print(f"   {variante}")

# Les variantes uniques : des parcours suivis par un seul cas
uniques = (comptage == 1).sum()
print(f"\nVariantes suivies par un seul cas : {uniques:,}")