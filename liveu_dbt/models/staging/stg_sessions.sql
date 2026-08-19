select
    session_id,
    device_id,
    customer_id,
    session_start::timestamp as session_start,
    duration_minutes,
    avg_bitrate_kbps,
    packet_loss_pct,
    uptime_pct,
    dropped_connection::boolean as dropped_connection,
    network_type
from {{ source('raw_data', 'raw_streaming_sessions') }}
where duration_minutes > 0