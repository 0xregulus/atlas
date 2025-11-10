with knowledge as (
    select tenant, article_id, title, updated_at from {{ ref('stg_knowledge_base') }}
),
usage as (
    select tenant, plan, tokens, requests from {{ source('core', 'tenant_usage') }}
)

select
    k.tenant,
    left(k.title, 50) as dataset_name,
    usage.plan,
    usage.tokens,
    usage.requests,
    k.updated_at as last_refresh
from knowledge k
left join usage on usage.tenant = k.tenant
