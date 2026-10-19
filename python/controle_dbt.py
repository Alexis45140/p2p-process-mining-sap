from pathlib import Path
import duckdb

RACINE = Path(__file__).resolve().parent.parent
con = duckdb.connect(str(RACINE / "data" / "p2p.duckdb"), read_only=True)

for table in ("fct_lignes_commande",):
    nb = con.sql(f"select count(*) from {table}").fetchone()[0]
    print(f"{table:<25} {nb:>10,}")

print("\nDurée des lignes de commande, en jours :")
print(con.sql("""
    select
        round(avg(duree_jours), 1)                              as moyenne,
        quantile_cont(duree_jours, 0.5)                         as mediane,
        max(duree_jours)                                        as maximum
    from fct_lignes_commande
""").df())