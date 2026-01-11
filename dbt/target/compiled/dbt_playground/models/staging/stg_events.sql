select
    event_id,
    user_id as customer_id,
    event_type,
    event_time
from "iceberg"."public_data"."events"