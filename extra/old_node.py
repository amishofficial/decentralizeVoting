from wallet import Wallet
from votechain import Votechain

class Node:

    def __init__(self):
        # self.id = str(uuid4())
        self.wallet = Wallet()
        self.wallet.create_keys()
        self.Votechain = Votechain(self.wallet.public_key)

    def get_vote_value(self):
        vote_given_to = input('Enter the party name to give vote to: ')
        return vote_given_to

    def get_user_choice(self):
        """Prompts the user for its choice and return it."""
        user_input = input('Your choice: ')
        return user_input

    # def get_walet_balance(self):
    #     token = self.wallet.amount
    #     return token

    def listen_for_input(self):
        waiting_for_input=True

        while waiting_for_input:
            print('Please choose')
            print('1: Login')
            print('2: Give vote')
            print('q: Quit')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                self.wallet.create_keys()
                print(self.wallet.public_key)
            elif user_choice == '2':
                vote_to = self.get_vote_value()
                signature = self.wallet.sign_vote(self.wallet.public_key, vote_to)
                if self.Votechain.add_vote(vote_to, self.wallet.public_key, signature):
                    self.wallet.vote_used()
                    print('Vote Added!')
                else:
                    print('Voting Failed!')
            elif user_choice == '3':
                self.Votechain.print_open_list()
            elif user_choice == 'q':
                waiting_for_input = False

if __name__ == '__main__':
    node = Node()
    node.listen_for_input()