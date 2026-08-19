select
    customer_id,
    customer_name,
    industry,
    region,
    segment,
    signup_date::date as signup_date
from {{ source('raw_data', 'raw_customers') }}