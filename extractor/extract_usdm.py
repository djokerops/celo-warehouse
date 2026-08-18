import sys
import pandas as pd
from web3 import Web3
 
from config import (USDM_ADDRESS, TRANSFER_TOPIC, LOG_CHUNK, DEFAULT_BLOCK_SPAN)
from rpc import latest_block, get_logs, get_block
from load import load_dataframe
 
 
def decode_transfer(log):
   # topics: [topic0, from(32b), to(32b)]; data = value (32b)
   frm = "0x" + log["topics"][1].hex()[-40:]
   to  = "0x" + log["topics"][2].hex()[-40:]
   value = int(log["data"].hex(), 16) if log["data"] else 0
   return {
       "block_number": log["blockNumber"],
       "tx_hash": log["transactionHash"].hex(),
       "log_index": log["logIndex"],
       "from_address": Web3.to_checksum_address(frm),
       "to_address": Web3.to_checksum_address(to),
       "raw_value": str(value),          # store as string; dbt casts to NUMERIC
   }
 
 
def run(block_span: int = DEFAULT_BLOCK_SPAN):
   tip = latest_block()
   start = tip - block_span
   print(f"Extracting USDm transfers from block {start:,} to {tip:,}")
 
   rows = []
   for lo in range(start, tip, LOG_CHUNK):
       hi = min(lo + LOG_CHUNK - 1, tip)
       logs = get_logs(USDM_ADDRESS, TRANSFER_TOPIC, lo, hi)
       rows.extend(decode_transfer(l) for l in logs)
       print(f"  blocks {lo:,}-{hi:,}: {len(logs)} logs (running total {len(rows):,})")
 
   if not rows:
       print("No logs found in window; exiting.")
       sys.exit(0)
 
   transfers = pd.DataFrame(rows)
 
   # Fetch timestamps for the distinct blocks we touched
   uniq_blocks = sorted(transfers["block_number"].unique())
   print(f"Fetching timestamps for {len(uniq_blocks):,} distinct blocks...")
   block_rows = []
   for b in uniq_blocks:
       blk = get_block(int(b))
       block_rows.append({
           "block_number": blk["number"],
           "block_timestamp": pd.to_datetime(blk["timestamp"], unit="s", utc=True),
           "gas_used": blk["gasUsed"],
           "tx_count": len(blk["transactions"]),
       })
   blocks = pd.DataFrame(block_rows)
 
   load_dataframe(transfers, "raw_usdm_transfers")
   load_dataframe(blocks, "raw_blocks")
   print("Extraction complete.")
 
 
if __name__ == "__main__":
   span = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_BLOCK_SPAN
   run(span)