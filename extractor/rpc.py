from web3 import Web3
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from config import RPC_URL
 
_w3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={"timeout": 30}))
 
def w3():
   if not _w3.is_connected():
       raise ConnectionError("Cannot reach Celo Forno RPC")
   return _w3
 
def latest_block() -> int:
   return w3().eth.block_number
 
@retry(
   reraise=True,
   stop=stop_after_attempt(6),
   wait=wait_exponential(multiplier=1, min=2, max=30),
   retry=retry_if_exception_type(Exception),
)
def get_logs(address: str, topic0: str, from_block: int, to_block: int):
   return w3().eth.get_logs({
       "address": Web3.to_checksum_address(address),
       "topics": [topic0],
       "fromBlock": from_block,
       "toBlock": to_block,
   })
 
@retry(
   reraise=True,
   stop=stop_after_attempt(6),
   wait=wait_exponential(multiplier=1, min=2, max=30),
)
def get_block(num: int):
   return w3().eth.get_block(num)