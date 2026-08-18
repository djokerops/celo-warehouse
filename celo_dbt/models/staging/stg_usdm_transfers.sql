WITH source AS(
    SELECT *
    FROM {{source('celo_raw', 'raw_usdm_transfers')}}
)

SELECT 
    tx_hash,
    block_number,
    log_index,
    lower(from_address) AS from_address,
    lower(to_address) AS to_address,
    cast(raw_value AS numeric)/1e18 AS amount_usdm

FROM source