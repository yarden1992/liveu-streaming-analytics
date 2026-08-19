select
    invoice_id,
    customer_id,
    device_id,
    invoice_date::date as invoice_date,
    amount_usd,
    status
from {{ source('raw_data', 'raw_invoices') }}