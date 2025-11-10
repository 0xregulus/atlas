with source as (
    select
        article_id,
        tenant,
        title,
        body,
        updated_at
    from {{ source('raw', 'knowledge_base') }}
)

select *
from source
