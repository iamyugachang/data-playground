
  create or replace view
    "iceberg"."public"."stg_customers"
  security definer
  as
    select
    id as customer_id,
    name,
    email
from "postgres"."public"."customers"
  ;
