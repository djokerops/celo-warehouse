WITH source AS(
    SELECT *  
    FROM {{ source('celo_raw', 'raw_blocks')}}
)

SELECT
    block_number,
    block_timestamp,
    date(block_timestamp) AS block_date,
    gas_used,
    tx_count
FROM source