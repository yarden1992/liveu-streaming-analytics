with invoices as (
    select * from {{ ref('stg_invoices') }}
),
customers as (
    select * from {{ ref('stg_customers') }}
),
devices as (
    select * from {{ ref('stg_devices') }}
)
select
    i.invoice_id,
    i.invoice_date,
    date_trunc('month', i.invoice_date) as invoice_month,
    to_char(i.invoice_date, 'Mon YYYY') as invoice_month_label,
	c.customer_name,
    c.region,
    c.segment,
    d.purchase_type,
    i.amount_usd,
    i.status
from invoices i
left join customers c on i.customer_id = c.customer_id
left join devices d on i.device_id = d.device_id