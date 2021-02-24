import hashlib as hl
import json

# __all__ = ['hash_string_256', 'hash_block']

def hash_string_256(string):
    """Create a SHA256 hash for a given input string.

    Arguments:
        :string: The string which should be hashed.
    """
    return hl.sha256(string).hexdigest()


def hash_vote(vote_block):
    """Hashes a block and returns a string representation of it.

    Arguments:
        :block: The block that should be hashed.
    """
    hashable_vote = vote_block.__dict__.copy()
    hashable_vote['votes'] = [tx.to_ordered_dict() for tx in hashable_vote['votes']]
    return hash_string_256(json.dumps(hashable_vote, sort_keys=True).encode())