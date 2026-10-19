select
    "case:concept:name"              as cas_id,
    "case:Purchasing Document"       as commande_id,
    "case:Item"                      as ligne,
    "concept:name"                   as activite,
    "time:timestamp"                 as horodatage,
    "User"                           as utilisateur,
    "case:Vendor"                    as fournisseur_id,
    "case:Name"                      as fournisseur_nom,
    "case:Company"                   as societe,
    "case:Document Type"             as type_document,
    "case:Item Category"             as type_rapprochement,
    "case:GR-Based Inv. Verif."      as controle_facture_sur_reception,
    "case:Goods Receipt"             as reception_attendue,
    "case:Spend area text"           as domaine_achat,
    "Cumulative net worth (EUR)"     as valeur_cumulee_eur
from {{ source('bpic', 'evenements') }}