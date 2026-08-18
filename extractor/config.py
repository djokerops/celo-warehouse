import os
from dotenv import load_dotenv
 
load_dotenv()  # reads .env from repo root
 
PROJECT_ID   = os.environ["GCP_PROJECT_ID"]
RAW_DATASET  = os.environ.get("BQ_RAW_DATASET", "celo_raw")
BQ_LOCATION  = os.environ.get("BQ_LOCATION", "africa-south1")
RPC_URL      = os.environ.get("CELO_RPC_URL", "https://forno.celo.org")
 
# USDm mainnet contract + ERC-20 Transfer topic0
USDM_ADDRESS   = "0x765DE816845861e75A25fCA122bb6898B8B1282a"
TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
 
# How many blocks per eth_getLogs call (keep modest for a public RPC)
LOG_CHUNK = 2000
 
# Backfill window size for a first run (blocks). ~1s blocks -> ~50k blocks/day.
DEFAULT_BLOCK_SPAN = 50_000