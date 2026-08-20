{{
    config(
        materialized = 'incremental',
        unique_key = ['tx_hash', 'log_index'],
        on_schema_change = 'sync_all_columns'
    )

}}





WITH transfers AS(
    SELECT *
    FROM {{ref('stg_usdm_transfers')}}
),
blocks AS(
    SELECT *
    FROM {{ ref('stg_blocks')}}
)

SELECT
    t.tx_hash,
    t.log_index,
    t.block_number,
    b.block_timestamp,
    b.block_date,
    t.from_address,
    t.to_address,
    t.amount_usdm
FROM transfers t 
INNER JOIN blocks b ON t.block_number = b.block_number

{% if is_incremental() %}
where b.block_number > (select coalesce(max(block_number), 0) from {{this}})
{% endif %}