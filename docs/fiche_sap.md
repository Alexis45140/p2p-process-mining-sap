# Où trouver quoi dans SAP pour le processus d'achat

Fiche pratique pour relier le journal d'événements du projet aux transactions et aux tables de SAP.

**À retenir :** le journal d'événements n'existe pas tel quel dans SAP. Il est reconstruit à partir de plusieurs tables : chaque étape du processus laisse une trace dans une table différente, et c'est leur assemblage, ligne de commande par ligne de commande, qui donne le parcours complet.

## Les étapes du processus

| Étape du processus | Transaction | Tables |
|---|---|---|
| Demande d'achat | ME51N | EBAN |
| Commande | ME21N | EKKO (en-tête), EKPO (lignes) ; historique de la commande : EKBE |
| Réception de la marchandise | MIGO | MKPF / MSEG, ou MATDOC en S/4HANA |
| Feuille de saisie de services | ML81N | ESSR / ESLL |
| Saisie de la facture | MIRO | RBKP (en-tête), RSEG (lignes) |
| Levée du blocage de paiement | MRBR | |
| Paiement | F110 | BSAK, ou ACDOCA en S/4HANA |
| Fournisseur (donnée de base) | | LFA1 |
| Article (donnée de base) | | MARA |

## Les colonnes du journal

| Colonne du journal | Champ SAP | Nom dans le projet |
|---|---|---|
| Purchasing Document | EKKO-EBELN (numéro de commande) | `commande_id` |
| Item | EKPO-EBELP (numéro de ligne) | `ligne` |
| Vendor | LFA1-LIFNR (fournisseur) | `fournisseur_id` |
| Company | BUKRS (société) | `societe` |
| Document Type | EKKO-BSART (type de commande) | `type_document` |
| GR-Based Inv. Verif. | EKPO-WEBRE (facture contrôlée sur la réception) | `controle_facture_sur_reception` |
| Goods Receipt | EKPO-WEPOS (réception attendue) | `reception_attendue` |
| User | ERNAM (auteur de l'enregistrement) | `utilisateur` |
| Cumulative net worth (EUR) | proche de EKPO-NETWR (valeur nette de la ligne) | `valeur_cumulee_eur` |

L'identifiant d'une ligne de commande (`cas_id`) est le numéro de commande suivi du numéro de ligne (EBELN + EBELP).

## Rapprochement à 2 et 3 voies, consignation

Le rapprochement est la vérification faite avant de payer une facture. Le type de rapprochement d'une ligne dépend des deux indicateurs de la commande : réception attendue (WEPOS) et facture contrôlée sur la réception (WEBRE).

- **Rapprochement à 3 voies** : la facture n'est payée que si la commande, la réception et la facture concordent.
  - *Facture après réception* (WEPOS et WEBRE cochés) : la facture est contrôlée par rapport à la réception.
  - *Facture avant réception* (WEPOS coché, WEBRE non coché) : la facture peut être saisie avant la réception, mais elle reste bloquée jusqu'à la réception. Le blocage est levé par un utilisateur ou par un traitement automatique. Payer une telle ligne avant la réception est donc une défaillance de contrôle : c'est le contrôle C1 du projet.
- **Rapprochement à 2 voies** (ni WEPOS ni WEBRE) : aucune réception n'est attendue. La facture est comparée à la commande seulement.
- **Consignation** : le fournisseur met du stock à disposition et l'entreprise ne paie que ce qu'elle consomme. Il n'y a pas de facture au niveau de la commande : la facturation passe par un processus séparé.

Répartition dans les données (251 652 lignes après nettoyage) :

| Type de rapprochement | Lignes | Part |
|---|---:|---:|
| 3 voies, facture avant réception | 220 948 | 87,8 % |
| 3 voies, facture après réception | 15 162 | 6,0 % |
| Consignation | 14 498 | 5,8 % |
| 2 voies | 1 044 | 0,4 % |
