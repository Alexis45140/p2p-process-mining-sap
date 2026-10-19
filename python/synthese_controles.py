from pathlib import Path
import duckdb

RACINE = Path(__file__).resolve().parent.parent
con = duckdb.connect(str(RACINE / "data" / "p2p.duckdb"), read_only=True)

print(con.sql("""
    select
        count(*)                                           as lignes,
        sum(c1_paye_avant_reception::int)                  as c1_paye_avant_reception,
        sum(c2_blocage_autre_motif::int)                   as c2_blocage_autre_motif,
        sum(c3_sans_demande_achat::int)                    as c3_sans_demande_achat,
        sum(c4_prix_modifie_apres_facture::int)            as c4_prix_modifie_apres_facture
    from fct_controles
""").df().T)

print("\nC1 par type de rapprochement :")
print(con.sql("""
    select type_rapprochement,
           count(*)                                     as lignes,
           sum(c1_paye_avant_reception::int)            as c1,
           round(avg(c1_paye_avant_reception::int) * 100, 2) as c1_pct
    from fct_controles
    group by type_rapprochement
    order by c1 desc
""").df())

print("\nDélai entre saisie de la facture et paiement, en jours :")
print(con.sql("""
    select
        quantile_cont(delai_paiement_jours, 0.5)  as mediane,
        quantile_cont(delai_paiement_jours, 0.9)  as neuvieme_decile,
        max(delai_paiement_jours)                 as maximum
    from fct_controles
    where delai_paiement_jours is not null
""").df())

print("\nC1 : montant en jeu et fournisseurs concernés :")
print(con.sql("""
    select
        count(*)                        as lignes,
        round(sum(valeur_eur))          as montant_eur,
        count(distinct fournisseur_id)  as fournisseurs
    from fct_controles
    where c1_paye_avant_reception
""").df())

print("\nC3 : part des lignes sans demande d'achat, par domaine :")
print(con.sql("""
    select domaine_achat,
           count(*)                                         as lignes,
           round(avg(c3_sans_demande_achat::int) * 100, 1)  as sans_demande_pct
    from fct_controles
    group by domaine_achat
    order by lignes desc
    limit 10
""").df())