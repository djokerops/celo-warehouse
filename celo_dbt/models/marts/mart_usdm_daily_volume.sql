WITH enriched AS(
    SELECT *
    FROM {{ ref('int_transfers_enriched')}}
)

SELECT 
    block_date,
    COUNT(*) AS transfer_count,
    COUNT(DISTINCT from_address) AS unique_senders,
    COUNT(DISTINCT to_address) AS unique_receivers,
    SUM(amount_usdm) AS total_volume,
    AVG(amount_usdm) AS average_transfer_usdm
FROM enriched
GROUP BY block_date
ORDER BY block_date