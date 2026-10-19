import os
import shutil
from collections import Counter
from pathlib import Path

GRAPHVIZ = r"C:\Program Files\Graphviz\bin"
if shutil.which("dot") is None and os.path.isdir(GRAPHVIZ):
    os.environ["PATH"] += os.pathsep + GRAPHVIZ

import duckdb
import graphviz

RACINE = Path(__file__).resolve().parent.parent
SORTIES = RACINE / "outputs"

# Libellés courts en français
LIBELLES = {
    "Create Purchase Requisition Item": "Demande\nd'achat",
    "Create Purchase Order Item": "Création de\nla commande",
    "Receive Order Confirmation": "Confirmation\ndu fournisseur",
    "Vendor creates invoice": "Facture émise\npar le fournisseur",
    "Record Goods Receipt": "Réception de\nla marchandise",
    "Record Invoice Receipt": "Saisie de\nla facture",
    "Remove Payment Block": "Levée du blocage\nde paiement",
    "Clear Invoice": "Paiement",
    "Delete Purchase Order Item": "Suppression\nde la ligne",
}

con = duckdb.connect(str(RACINE / "data" / "p2p.duckdb"), read_only=True)
df = con.sql("select cas_id, activite, horodatage from int_evenements_valides").df()
df = df.sort_values(["cas_id", "horodatage"], kind="stable")

# Variante de chaque cas, sous forme de tuple d'étapes
variantes = df.groupby("cas_id")["activite"].agg(tuple).value_counts()
top10 = variantes.head(10)

# Compter les passages d'une étape à la suivante, pour les 10 variantes
aretes = Counter()
aretes_ideales = set()
for rang, (etapes, nb) in enumerate(top10.items(), start=1):
    chemin = ["Début"] + [LIBELLES.get(e, e) for e in etapes] + ["Fin"]
    for a, b in zip(chemin, chemin[1:]):
        aretes[(a, b)] += nb
        if rang <= 2:                      # V1 et V2 : le parcours sans accroc
            aretes_ideales.add((a, b))

maximum = max(aretes.values())

g = graphviz.Digraph(format="png")
g.attr(rankdir="LR", dpi="200", bgcolor="white", nodesep="0.35", ranksep="0.45")
g.attr("node", shape="box", style="rounded,filled", fillcolor="#2F3E46",
       fontcolor="white", fontname="Segoe UI", fontsize="22", margin="0.2,0.1")
g.attr("edge", fontname="Segoe UI", fontsize="18", fontcolor="#6B7A80")

for extremite in ("Début", "Fin"):
    g.node(extremite, shape="circle", fillcolor="#E07A1F", fontsize="14", width="0.9")

for (a, b), nb in aretes.items():
    ideale = (a, b) in aretes_ideales
    g.edge(
        a, b,
        label=f"{nb:,}".replace(",", " "),
        penwidth=str(1 + 7 * nb / maximum),
        color="#E07A1F" if ideale else "#9AA5A9",
    )

g.render(SORTIES / "carte_processus_fr", cleanup=True)
print("Carte écrite :", SORTIES / "carte_processus_fr.png")