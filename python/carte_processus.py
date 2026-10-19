import os
import shutil

# Rendre Graphviz accessible même si le PATH du terminal n'est pas à jour
GRAPHVIZ = r"C:\Program Files\Graphviz\bin"
if shutil.which("dot") is None and os.path.isdir(GRAPHVIZ):
    os.environ["PATH"] += os.pathsep + GRAPHVIZ


from pathlib import Path
import duckdb
import pm4py

RACINE = Path(__file__).resolve().parent.parent
SORTIES = RACINE / "outputs"
SORTIES.mkdir(exist_ok=True)

con = duckdb.connect(str(RACINE / "data" / "p2p.duckdb"), read_only=True)
df = con.sql("select cas_id, activite, horodatage from int_evenements_valides").df()

# Indiquer à PM4Py quelles colonnes jouent les rôles de cas, d'activité et d'horodatage
journal = pm4py.format_dataframe(
    df, case_id="cas_id", activity_key="activite", timestamp_key="horodatage"
)

# Carte 1 : le processus complet, toutes variantes confondues
dfg, debuts, fins = pm4py.discover_dfg(journal)
pm4py.save_vis_dfg(dfg, debuts, fins, str(SORTIES / "carte_complete.png"))
print("Carte complète écrite")

# Carte 2 : les 10 variantes principales, en fréquence
# Filtrer les 10 variantes principales nous-mêmes
# (la fonction de PM4Py est incompatible avec le format texte récent de Pandas)
journal_trie = journal.sort_values(["case:concept:name", "time:timestamp"], kind="stable")
variante_par_cas = journal_trie.groupby("case:concept:name")["concept:name"].agg(" → ".join)
top10 = variante_par_cas.value_counts().head(10).index
cas_principaux = variante_par_cas[variante_par_cas.isin(top10)].index
principal = journal[journal["case:concept:name"].isin(cas_principaux)]
dfg, debuts, fins = pm4py.discover_dfg(principal)
pm4py.save_vis_dfg(dfg, debuts, fins, str(SORTIES / "carte_frequence.png"))
print("Carte des fréquences écrite")

# Carte 3 : les mêmes variantes, avec le délai médian de chaque passage
dfg_perf, debuts, fins = pm4py.discover_performance_dfg(principal)
pm4py.save_vis_performance_dfg(
    dfg_perf, debuts, fins,
    str(SORTIES / "carte_delais.png"),
    aggregation_measure="median",
)
print("Carte des délais écrite")