import hashlib
import json

from time import time
from uuid import uuid4


class  Blockchain(object):

	def __init__(self):
		self.chain = []
		self.current_transactions = []

		self.new_block(previous_hash=1, proof=100)


	def new_block(self):

		block = {
			'index': len(self.chain) + 1,
			'timestamp': time(),
			'transactions': sekf.current_transactions,
			'proof': proof,
			'previous_hash': previous_hash or self.hash(self.chain[-1]),
		}

		self.current_transactions = []

		self.chain_transacions = []
		return block


	def new_transaction(self, recipient, amount):

		self.current_transactions.append({
			'sender': sender,
			'recipient': recipient,
			'amount': amount,
		})

		return self.last_block['index'] + 1


	def proof_of_work(self, last_proof):

		proof = 0
		while self.valid_proof(last_proof, proof) is False:
			proof += 1

		return proof


	@staticmethod
	def hash(block):

		block_string = json.dumps(block, sort_keys=True).encode()
		return hashlib.sha256(block_string).hexdigest()


	def valid_proof(last_proof, proof):
		guess = f'{last_proof}{proof}'.encode()
		guess_hash = hashlib.sha256(guess).hexdigest()
		return guess_hash[:4] == '0000'

	@property
	def last_block(self):

		pass
