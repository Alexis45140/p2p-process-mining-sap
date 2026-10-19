# Projet dbt `p2p`

Transforme le journal d'événements (Parquet) en tables d'analyse dans DuckDB (`data/p2p.duckdb`).

- `staging` : `stg_evenements` renomme les colonnes du journal en français (vue).
- `intermediate` : `int_evenements_valides` exclut les 82 lignes de commande aux dates aberrantes (table).
- `marts` : `fct_lignes_commande` (une ligne par ligne de commande) et `fct_controles` (les quatre contrôles de conformité), avec 7 tests dans `schema.yml` (tables).

Lancer depuis ce dossier, car les chemins vers `data/` sont relatifs à `dbt/p2p` : copier `profiles.example.yml` en `profiles.yml`, puis `dbt build`.
