with dates_cles as (
    select
        cas_id,
        min(horodatage) filter (where activite = 'Create Purchase Requisition Item') as date_demande_achat,
        min(horodatage) filter (where activite = 'Record Goods Receipt')             as date_premiere_reception,
        min(horodatage) filter (where activite = 'Record Invoice Receipt')           as date_premiere_facture,
        min(horodatage) filter (where activite = 'Clear Invoice')                    as date_paiement,
        max(horodatage) filter (where activite = 'Change Price')                     as date_dernier_changement_prix,
        count(*)        filter (where activite = 'Remove Payment Block')             as nb_levees_blocage
    from {{ ref('int_evenements_valides') }}
    group by cas_id
)

select
    f.cas_id,
    f.type_rapprochement,
    f.domaine_achat,
    f.fournisseur_id,
    f.valeur_eur,
    d.*  exclude (cas_id),

    date_diff('day', d.date_premiere_facture, d.date_paiement) as delai_paiement_jours,

    -- C1 : payée avant la réception, alors qu'un rapprochement à 3 voies l'exige
    coalesce(
        f.type_rapprochement like '3-way%'
        and d.date_paiement is not null
        and (d.date_premiere_reception is null
             or d.date_paiement < d.date_premiere_reception),
        false
    ) as c1_paye_avant_reception,

    -- C2 : blocage levé alors que la réception précédait la facture
    coalesce(
        d.nb_levees_blocage > 0
        and d.date_premiere_reception < d.date_premiere_facture,
        false
    ) as c2_blocage_autre_motif,

    -- C3 : commande créée sans demande d'achat
    d.date_demande_achat is null as c3_sans_demande_achat,

    -- C4 : prix modifié après la saisie de la facture
    coalesce(
        d.date_dernier_changement_prix > d.date_premiere_facture,
        false
    ) as c4_prix_modifie_apres_facture

from {{ ref('fct_lignes_commande') }} as f
left join dates_cles as d using (cas_id)