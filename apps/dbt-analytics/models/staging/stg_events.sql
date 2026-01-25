select
    event_id,
    user_id as customer_id,
    event_type,
    event_time
from {{ source('raw_events', 'events') }}
