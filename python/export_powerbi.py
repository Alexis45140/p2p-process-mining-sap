from pathlib import Path
import duckdb

RACINE = Path(__file__).resolve().parent.parent
SORTIE = RACINE / "outputs" / "powerbi"
SORTIE.mkdir(parents=True, exist_ok=True)

con = duckdb.connect(str(RACINE / "data" / "p2p.duckdb"), read_only=True)
controles = con.sql("""
    select c.*, l.duree_jours
    from fct_controles c
    left join fct_lignes_commande l using (cas_id)
""").df()
evenements = con.sql(
    "select cas_id, activite, horodatage from int_evenements_valides"
).df()

# Variante de chaque cas
evenements = evenements.sort_values(["cas_id", "horodatage"], kind="stable")
variante = evenements.groupby("cas_id")["activite"].agg(" → ".join)

# Libellés courts pour les 10 variantes principales, dans l'ordre de fréquence
libelles = [
    "V1 Facture datée avant réception",
    "V2 Réception puis facture",
    "V3 Sans facture",
    "V4 V1 et levée de blocage",
    "V5 Avec confirmation",
    "V6 Avec demande d'achat",
    "V7 Facture bloquée",
    "V8 V2 et levée de blocage",
    "V9 Ligne supprimée",
    "V10 Confirmation puis facture",
]

top10 = variante.value_counts().head(10).index
correspondance = dict(zip(top10, libelles))

controles["variante"] = (
    controles["cas_id"].map(variante).map(correspondance).fillna("Autres parcours")
)
controles["parcours_ideal"] = controles["variante"].str.startswith(("V1 ", "V2 "))

controles.to_parquet(SORTIE / "controles.parquet", index=False)
print("Lignes exportées :", len(controles))
print(controles["variante"].value_counts())