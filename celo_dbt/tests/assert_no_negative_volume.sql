SELECT *
FROM {{ref('mart_usdm_daily_volume')}}
WHERE total_volume < 0