with customers as (
    select * from {{ ref('stg_customers') }}
),
events as (
    select * from {{ ref('stg_events') }}
)
select
    c.customer_id,
    c.name,
    count(e.event_id) as total_events
from customers c
left join events e on c.customer_id = e.customer_id
group by 1, 2
