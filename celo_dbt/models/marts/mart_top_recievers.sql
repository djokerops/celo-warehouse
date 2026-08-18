WITH enriched AS(
    SELECT *
    FROM {{ ref('int_transfers_enriched')}}
)

SELECT
    to_address,
    COUNT(*) AS transfer_received,
    SUM(amount_usdm) AS total_usdm_received
FROM enriched
GROUP BY to_address
ORDER BY 3 DESC