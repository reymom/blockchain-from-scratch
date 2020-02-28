from flask import jsonify, render_template, request
from flask_cors import CORS
from app import app
from app.models import Blockchain


CORS(app)
blockchain = Blockchain()

MINING_REWARD = 1
MINING_SENDER = "THE BLOCKCHAIN"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/configure')
def configure():
    return render_template('configure.html')


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    print('new transaction')
    values = request.form
    required = ['sender_address', 'recipient_address', 'amount', 'signature']
    if not all(k in values for k in required):
        return 'Missing values', 400
    transaction_result = blockchain.submit_transaction(
        values['sender_address'],
        values['recipient_address'],
        values['amount'],
        values['signature']
    )
    if not transaction_result:
        return jsonify({'message': 'Invalid Transaction'}), 406
    else:
        response = {'message': 'Transaction will be added to Block {}'.format(transaction_result)}
        return jsonify(response), 201


@app.route('/transactions/get', methods=['GET'])
def get_transactions():
    # print('\nHola get_transactions')
    transactions = blockchain.transactions
    # print(transactions)
    return jsonify({'transactions': transactions}), 200


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/mine', methods=['GET'])
def mine():
    # print('Hola minero')
    last_block = blockchain.chain[-1]
    # print(last_block)
    nonce = blockchain.proof_of_work()
    # print(nonce)
    blockchain.submit_transaction(
        sender_address=MINING_SENDER,
        recipient_address=blockchain.node_id,
        value=MINING_REWARD,
        signature=""
    )
    previous_hash = blockchain.hash(last_block)
    block = blockchain.create_block(nonce, previous_hash)

    response = {
        'message': 'New Forged Block',
        'block_number': block['block_number'],
        'transactions': block['transactions'],
        'nonce': block['nonce'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response, 200)


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.form
    nodes = values.get('nodes').replace(" ", "").split(',')
    if nodes is None:
        return "ERROR: please supply a valid list of nodes", 400
    for node in nodes:
        blockchain.register_node(node)
    response = {
        'message': 'New nodes added',
        'total_nodes': [node for node in blockchain.nodes]
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()
    if replaced:
        response = {
            'message': 'Our Chain is Replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our Chain is Principal',
            'new_chain': blockchain.chain
        }
    return jsonify(response), 200


@app.route('/nodes/get', methods=['GET'])
def get_nodes():
    nodes = list(blockchain.nodes)
    response = {'nodes': nodes}
    return jsonify(response), 200
