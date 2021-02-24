from flask import Flask, jsonify, request, send_from_directory,render_template
from flask_cors import CORS

from wallet import Wallet
from votechain import Votechain

app = Flask(__name__)
voters=[]

CORS(app)

@app.route('/', methods=['GET','POST'])
def get_node_ui():
    global votechain
    wallet.create_keys()
    votechain = Votechain(wallet.public_key, port)
    return render_template('Register.html')

@app.route('/network', methods=['GET','POST'])
def get_network_ui():
    return send_from_directory('templates', 'network.html')

@app.route('/keys.html', methods=['GET','POST'])
def logged_in():
    global votechain
    global voters
    if request.method=='POST':
       voter_id=request.form['voter_id']
       if voter_id in voters:
           print("USER HAS ALREADY VOTED!!!!!!")
           return render_template('Register.html')
       voters.append(voter_id)
       voter_name=request.form['voter_name']
       if (voter_id != "" and voter_name != ""):
            wallet.create_keys()
            # votechain = Votechain(wallet.public_key)
            return render_template('keys.html', priv_key=wallet.private_key, pub_key=wallet.public_key)


@app.route('/vote.html', methods=['GET','POST'])
def vote():
    # wallet.create_keys()
    # votechain = Votechain(wallet.public_key)
    return render_template('vote.html')


@app.route('/Result.html', methods=['GET','POST'])
def result():
    global votechain
    global voters
    p1=p2=0
    if request.method=='POST':
        vote_to=request.form['vote_given_to']
        if vote_to=="ABC":
            p1 = p1+1
        if vote_to=="BCD":
            p2 = p2+1
        private_key = request.form['priv_key']
    if private_key==wallet.private_key:
        signature = wallet.sign_vote(wallet.public_key, vote_to)
        if votechain.add_vote(vote_to, wallet.public_key, signature):
            wallet.vote_used()
            print('Vote Added!')
            print("No. of Voters: "+str(len(voters)))
            mb = int(len(voters)/3)
            print("No of Mined Blocks: "+ str(mb))
            print("Votes for ABC : "+ str(p1))
            print("Votes for BCD : "+ str(p2))
        else:
            print('Voting Failed!')
    return render_template('Result.html')
       
@app.route('/Register.html', methods=['GET','POST'])
def get_ui_again():
    # wallet.create_keys()
    # votechain = Votechain(wallet.public_key)
    return render_template('Register.html')

@app.route('/node', methods=['POST'])
def add_node():
    values = request.get_json()
    if not values:
        response={
            'message':'No data attachd'
        }
        return jsonify(response), 400
    if 'node' not in values:
        response={
            'message':'No node data found'
        }
        return jsonify(response), 400
    node = values['node']
    votechain.add_peer_node(node)
    response={
            'message':'No node data found',
            'all_nodes':votechain.get_peer_nodes()
        }
    return jsonify(response), 201

@app.route('/node/<node_url>', methods=['DELETE'])
def remove_node(node_url):
    if node_url=="" or node_url==None:
        response={
            'message':'No node attachd'
        }
        return jsonify(response), 400
    votechain.remove_peer_node(node_url)
    response={
            'message':'Node removed',
            'all_nodes':votechain.get_peer_nodes()
        }
    return jsonify(response), 200

@app.route('/nodes', methods=['GET','POST'])
def get_nodes():
    nodes = votechain.get_peer_nodes()
    if nodes:
        response={
            'all_nodes':nodes
        }
        return jsonify(response), 200

if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p','--port',type = int,default = 5000)
    args = parser.parse_args()
    port = args.port
    wallet = Wallet()
    votechain = Votechain(wallet.public_key,port)
    app.run(host='0.0.0.0', port = port)
