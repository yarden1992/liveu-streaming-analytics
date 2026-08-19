with sessions as (
    select * from {{ ref('stg_sessions') }}
),
devices as (
    select * from {{ ref('stg_devices') }}
),
customers as (
    select * from {{ ref('stg_customers') }}
)
select
    s.session_id,
    s.session_start,
    d.device_model,
    d.purchase_type,
    c.customer_name,
    c.industry,
    c.region,
    s.duration_minutes,
    s.avg_bitrate_kbps,
    s.uptime_pct,
    s.dropped_connection,
    s.network_type,
    case
        when s.uptime_pct >= 99 then 'Excellent'
        when s.uptime_pct >= 95 then 'Good'
        else 'Needs Attention'
    end as reliability_tier
from sessions s
left join devices d on s.device_id = d.device_id
left join customers c on s.customer_id = c.customer_id