from vote_block import Vote_Block
from wallet import Wallet
import json
from functools import reduce
from utility.hash_util import hash_vote
from utility.verification import Verification
import pickle
from Vote import Vote
import hashlib as hl


# Login_Reward = 1

class Votechain:
    def __init__(self,voter_public_key, node_id):
        genesis_vote= Vote_Block(0,'',[],100,0)
        self.votechain = [genesis_vote]
        self.__open_transactions =[]
        # self.voter_public_key = voter_public_key
        # print("1")
        self.hosting_node = voter_public_key
        self.__peer_nodes = set()
        self.node_id = node_id
        self.load_data()
    
    @property
    def votechain(self):
        return self.__votechain[:]

    @votechain.setter 
    def votechain(self, val):
        self.__votechain = val

    def get_open_transactions(self):
        return self.__open_transactions[:] 
    
    def load_data(self):
        try:
            with open('votechain-{}.txt'.format(self.node_id), mode='r') as f:
                # file_content = pickle.loads(f.read())
                file_content = f.readlines()
                # blockchain = file_content['chain']
                # open_transactions = file_content['ot']
                votechain = json.loads(file_content[0][:-1])
                # We need to convert  the loaded data because Transactions should use OrderedDict
                updated_blockchain = []
                for block in votechain:
                    converted_tx = [Vote(
                        tx['sender'], tx['recipient'], tx['signature']) for tx in block['votes']]
                    updated_block = Vote_Block(
                        block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.votechain = updated_blockchain
                open_transactions = json.loads(file_content[1][:-1])
                # We need to convert  the loaded data because Transactions should use OrderedDict
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Vote(
                        tx['voter'], tx['vote_to'], tx['signature'])
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
                peer_nodes = json.loads(file_content[2])
                self.__peer_nodes = set(peer_nodes)
        except (IOError, IndexError):
            pass
        finally:
            print('Cleanup!')
    
    def save_data(self):
        try:
            with open('votechain-{}.txt'.format(self.node_id), mode='w') as f:
                saveable_chain = [vote.__dict__ for vote in [Vote_Block(vote_el.index, vote_el.previous_hash, [
                    tx.__dict__ for tx in vote_el.votes], vote_el.proof, vote_el.timestamp) for vote_el in self.__votechain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_tx))
                f.write('\n')
                f.write(json.dumps(list(self.__peer_nodes)))
                # save_data = {
                #     'chain': blockchain,
                #     'ot': open_transactions
                # }
                # f.write(pickle.dumps(save_data))
        except IOError:
            print('Saving failed!')
    
    def save_database(self):
        try:
            with open('database.txt', mode='a') as f:
                f.write(self.sender)
                f.write('\t\t\t')
                f.write(self.vote_to)
                f.write('\n')
        except IOError:
            print('Saving failed!')

    def proof_of_work(self):
        """Generate a proof of work for the open transactions, the hash of the previous block and a random number (which is guessed until it fits)."""
        last_block = self.__votechain[-1]
        last_hash = hash_vote(last_block)
        proof = 0
        # Try different PoW numbers and return the first valid one
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balance(self):
        # # """Calculate and return the balance for a participant."""
        # if self.hosting_node == None:
        #     # print("2")            
        #     return None
        # # participant = self.hosting_node
        # if self.wallet.amount == 1.0:
        #     print ("5")
        #     return self.wallet.amount
        # am = Node.get_walet_balance()
        am = 1.0
        return am

    def add_vote(self, vote_to, sender, signature):
        if self.hosting_node == None:
            return False
        self.vote_to= vote_to
        self.sender = sender
        vote = Vote(sender, vote_to, signature)
        if Verification.verify_vote(vote, self.get_balance):
            self.__open_transactions.append(vote)
            self.save_data()
            self.save_database()
            if len(self.__open_transactions)==3:
                self.mine_block()       
            return True
        return False
        

    def mine_block(self):
        """Create a new block and add open transactions to it."""
        # Fetch the currently last block of the blockchain
        if self.hosting_node == None:
            return None
        last_block = self.__votechain[-1]
        # Hash the last block (=> to be able to compare it to the stored hash value)
        hashed_block = hash_vote(last_block)
        proof = self.proof_of_work()
        # Miners should be rewarded, so let's create a reward transaction
        # reward_transaction = {
        #     'sender': 'MINING',
        #     'recipient': owner,
        #     'amount': MINING_REWARD
        # }

        # reward_transaction = Vote('_INIT', self.hosting_node, '')

        # Copy transaction instead of manipulating the original open_transactions list
        # This ensures that if for some reason the mining should fail, we don't have the reward transaction stored in the open transactions
        copied_transactions = self.__open_transactions[:]
        for vt in copied_transactions:
            if not Wallet.verify_vote(vt):
                return None
        # copied_transactions.append(reward_transaction)
        vote = Vote_Block(len(self.__votechain), hashed_block,
                      copied_transactions, proof)
        self.__votechain.append(vote)
        self.__open_transactions = []
        self.save_data()
        return vote

    def print_open_list(self):
        print( self.__open_transactions)

    def add_peer_node(self, node):
        """Adds a new node to the peer node set.

        Arguments:
            :node: The node URL which should be added.
        """
        self.__peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node):
        """Removes a node from the peer node set.

        Arguments:
            :node: The node URL which should be removed.
        """
        self.__peer_nodes.discard(node)
        self.save_data()

    def get_peer_nodes(self):
        """Return a list of all connected peer nodes."""
        return list(self.__peer_nodes)