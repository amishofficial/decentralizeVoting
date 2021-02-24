"""Provides verification helper methods."""

from utility.hash_util import hash_string_256, hash_vote
from wallet import Wallet

class Verification:
    """A helper class which offer various static and class-based verification and validation methods."""
    @staticmethod
    def valid_proof(votes, last_hash, proof):
        """Validate a proof of work number and see if it solves the puzzle algorithm (two leading 0s)

        Arguments:
            :votes: The votes of the block for which the proof is created.
            :last_hash: The previous block's hash which will be stored in the current block.
            :proof: The proof number we're testing.
        """
        # Create a string with all the hash inputs
        guess = (str([vt.to_ordered_dict() for vt in votes]) + str(last_hash) + str(proof)).encode()
        # Hash the string
        # IMPORTANT: This is NOT the same hash as will be stored in the previous_hash. It's a not a block's hash. It's only used for the proof-of-work algorithm.
        guess_hash = hash_string_256(guess)
        # print(guess_hash)
        # Only a hash (which is based on the above inputs) which starts with two 0s is treated as valid
        # This condition is of course defined by you. You could also require 10 leading 0s - this would take significantly longer (and this allows you to control the speed at which new blocks can be added)
        return guess_hash[0:2] == '00'
        
    @classmethod
    def verify_chain(cls, Votechain):
        """ Verify the current blockchain and return True if it's valid, False otherwise."""
        for (index, vote_block) in enumerate(Votechain):
            if index == 0:
                continue
            if vote_block.previous_hash != hash_vote(Votechain[index - 1]):
                return False
            if not cls.valid_proof(vote_block.votes[:-1], vote_block.previous_hash, vote_block.proof):
                print('Proof of work is invalid')
                return False
        return True

    @staticmethod
    def verify_vote(vote, get_balance, check_funds=True):
        """Verify a vote by checking whether the sender has sufficient coins.

        Arguments:
            :vote: The vote that should be verified.
        """
        if check_funds:
            sender_balance = get_balance()
            # print(sender_balance)
            return sender_balance == 1.0 and Wallet.verify_vote(vote)
        else:
            return Wallet.verify_vote(vote)

    @classmethod
    def verify_votes(cls, open_transactions, get_balance):
        """Verifies all open votes."""
        return all([cls.verify_vote(tx, get_balance, False) for tx in open_transactions])