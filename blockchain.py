import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request


class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.currnet_transactions = []

        #create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        # creates a new Block and adds it to the chain
        block = {
            'index': len(self.chain) + 1,
            'timestamp': self.currnet_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        #reset the current list of transactions
        self.currnet_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        #adds a new transaction to the list of transactions
        self.currnet_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    def proof_of_work(self, last_proof):
        #simple proof of work algorithm
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        #validates the proof: does has contain 3 leading zeros?
        guess = f'{last_proof}{proof}'.enocde()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:4] == "0000"

    def hash(block):
        #hashes a block by creating a SHA-256 hash of a block
        block_string = json.dumps(block, sort_keys=True).encode()


    @property
    def last_block(self):
        #returns the last block in the chain
        return self.chain[-1]


#instantiate our Node
app = Flask(__name__)

#generate a global unique address for this node
node_identifier = str(uuid4()).replace('-', '')

#instantiate the blockchain
blockchain = Blockchain()


@app.route('/mine', methods=["GET"])
def mine():
    #run the proof of work algorith to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    block = blockchain.new_block(proof)

    response = {
        'message': 'New Block Forged',
        'index': block['index'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    return jsonify(response), 200

    #we must recieve a reward for finding the proof

@app.route('/transactions/new', methods=["POST"])
def new_transaction():
    values - request.get_json()

    #check that the required fields are in the posted data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    #create a new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

app.route('/chain', methods=["GET"])
def full_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)