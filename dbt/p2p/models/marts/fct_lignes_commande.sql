select
    cas_id,
    any_value(commande_id)             as commande_id,
    any_value(ligne)                   as ligne,
    any_value(fournisseur_id)          as fournisseur_id,
    any_value(fournisseur_nom)         as fournisseur_nom,
    any_value(societe)                 as societe,
    any_value(type_document)           as type_document,
    any_value(type_rapprochement)      as type_rapprochement,
    any_value(domaine_achat)           as domaine_achat,

    min(horodatage)                    as premier_evenement,
    max(horodatage)                    as dernier_evenement,
    date_diff('day', min(horodatage), max(horodatage)) as duree_jours,

    count(*)                                                        as nb_etapes,
    count(*) filter (where activite = 'Record Goods Receipt')       as nb_receptions,
    count(*) filter (where activite = 'Record Invoice Receipt')     as nb_factures,
    count(*) filter (where activite like 'Change%')                 as nb_modifications,
    max(valeur_cumulee_eur)                                         as valeur_eur

from {{ ref('int_evenements_valides') }}
group by cas_id