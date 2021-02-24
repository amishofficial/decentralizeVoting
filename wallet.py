from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random
import binascii


class Wallet:
    """Creates, loads and holds private and public keys. Manages transaction signing and verification."""

    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.amount = 0.0

    def create_keys(self):
        """Create a new pair of private and public keys."""
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key
        self.amount = 1.0

    def get_balance_wallet(self):
        balance = self.amount
        return balance
    # def save_keys(self):
    #     """Saves the keys to a file (wallet.txt)."""
    #     if self.public_key != None and self.private_key != None:
    #         try:
    #             with open('wallet.txt', mode='w') as f:
    #                 f.write(self.public_key)
    #                 f.write('\n')
    #                 f.write(self.private_key)
    #             return True
    #         except (IOError, IndexError):
    #             print('Saving wallet failed...')
    #             return False

    # def load_keys(self):
    #     """Loads the keys from the wallet.txt file into memory."""
    #     try:
    #         with open('wallet.txt', mode='r') as f:
    #             keys = f.readlines()
    #             public_key = keys[0][:-1]
    #             private_key = keys[1]
    #             self.public_key = public_key
    #             self.private_key = private_key
    #         return True
    #     except (IOError, IndexError):
    #         print('Loading wallet failed...')
    #         return False

    def generate_keys(self):
        """Generate a new pair of private and public key."""
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        return (binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii'))

    def sign_vote(self, voter, vote_to):
        """Sign a transaction and return the signature.

        Arguments:
            :voter: The voter of the transaction.
            :vote_to: The vote_to of the transaction.
        """
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(self.private_key)))
        h = SHA256.new((str(voter) + str(vote_to)).encode('utf8'))
        signature = signer.sign(h)
        return binascii.hexlify(signature).decode('ascii')

    @staticmethod
    def verify_vote(vote):
        """Verify the signature of a transaction.

        Arguments:
            :transaction: The transaction that should be verified.
        """
        public_key = RSA.importKey(binascii.unhexlify(vote.voter))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA256.new((str(vote.voter) + str(vote.vote_to)).encode('utf8'))
        return verifier.verify(h, binascii.unhexlify(vote.signature))

    def vote_used(self):
        self.amount=0.0
