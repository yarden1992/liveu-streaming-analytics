select
    device_id,
    customer_id,
    device_model,
    purchase_type,
    activation_date::date as activation_date
from {{ source('raw_data', 'raw_devices') }}