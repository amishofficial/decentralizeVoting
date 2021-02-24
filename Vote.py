from collections import OrderedDict

from utility.printable import Printable

class Vote(Printable):
    """A transaction which can be added to a vote_block in the votechain.

    Attributes:
        :voter: The voter of the coins.
        :vote_to: The vote_to of the coins.
        :signature: The signature of the transaction.
        :amount:
    """
    def __init__(self, voter, vote_to, signature):
        self.voter = voter
        self.vote_to = vote_to
        self.signature = signature

    def to_ordered_dict(self):
        """Converts this transaction into a (hashable) OrderedDict."""
        return OrderedDict([('voter', self.voter), ('vote_to', self.vote_to)])
