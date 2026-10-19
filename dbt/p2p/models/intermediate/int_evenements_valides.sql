-- Exclut les cas entiers dont au moins un événement a une date aberrante
with cas_aberrants as (
    select distinct cas_id
    from {{ ref('stg_evenements') }}
    where year(horodatage) not between 2017 and 2019
)

select e.*
from {{ ref('stg_evenements') }} as e
where e.cas_id not in (select cas_id from cas_aberrants)