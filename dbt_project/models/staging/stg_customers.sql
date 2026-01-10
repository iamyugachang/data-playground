select
    id as customer_id,
    name,
    email
from {{ source('shop', 'customers') }}
