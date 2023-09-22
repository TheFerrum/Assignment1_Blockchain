import hashlib
import time
from collections import defaultdict


class Account:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance

    def __str__(self):
        return f"{self.name}'s Account (Balance: {self.balance})"
    
    def get_name(self):
        return self.name
    
    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
        else:
            print("Insufficient balance")

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
    
    def is_executable(self):
        if self.sender.balance >= self.amount:
            print(f"Transaction can be successful: {self.sender.name} can sent {self.amount} to {self.recipient.name}")
            return True
        else:
            print(f"Transaction failed: Insufficient balance in sender {self.sender.name}'s account")
            return False
    
    def execute_transaction(self):
        self.sender.withdraw(self.amount)
        self.recipient.deposit(self.amount)
        print(f"Transaction successful: {self.sender.name} sent {self.amount} to {self.recipient.name}")
        
class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, nonce):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.merkle_root = self.calculate_merkle_root()
        self.hash = self.calculate_hash()

    def calculate_merkle_root(self):
        # Calculate the Merkle root from the list of transaction data
        list_of_transaction_data =[]
        for transaction in self.transactions:
            if transaction.is_executable():
                transaction.execute_transaction()
                transaction_data = transaction.sender.get_name() + transaction.recipient.get_name() + str(transaction.amount)
                list_of_transaction_data.append(transaction_data)
        
        transaction_hashes = self.calculate_transaction_hashes(list_of_transaction_data)
        
        if not transaction_hashes:
            return "0"
        
        while len(transaction_hashes) > 1:
            next_level = []
            for i in range(0, len(transaction_hashes), 2):
                hash_pair = transaction_hashes[i] + (transaction_hashes[i+1] if i+1 < len(transaction_hashes) else transaction_hashes[i])
                next_level.append(hashlib.sha256(hash_pair.encode()).hexdigest())
            transaction_hashes = next_level
        return transaction_hashes[0]

    def calculate_transaction_hashes(self, transaction_data):
        # Calculate the SHA-256 hash for each transaction data
        return [hashlib.sha256(data.encode()).hexdigest() for data in transaction_data]

    def calculate_hash(self):
        data = str(self.index) + self.previous_hash + str(self.timestamp) + self.merkle_root + str(self.nonce)
        return hashlib.sha256(data.encode()).hexdigest()

    def is_valid(self):
        # Check if the block's hash starts with a given number of leading zeros (proof-of-work)
        difficulty = 2 
        if self.hash[:difficulty] != '0' * difficulty:
            return False
        
        return True

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []

    def create_genesis_block(self):
        return Block(0, "0", int(time.time()), [], 0)

    def get_latest_block(self):
        return self.chain[-1]

    def mine_pending_transactions(self, miner_account):        
        blockchain_reward = Account("Blockchain_Reward", 0.01)
        reward_transaction = Transaction(blockchain_reward, miner_account, 0.01)
        self.pending_transactions.append(reward_transaction)
        
        new_block = Block(len(self.chain), self.get_latest_block().hash, int(time.time()), self.pending_transactions, 0)
        self.pending_transactions = []
        new_block.nonce = self.proof_of_work(new_block)

        # Check if the new block is valid before adding it to the chain
        if new_block.is_valid():
            self.chain.append(new_block)
            print(f"Block #{new_block.index} has been mined and added to the chain!")
            return new_block
        else:
            print("Invalid block! Block was not added to the chain.")
            return None

    def proof_of_work(self, block, difficulty = 2):
        while block.hash[:difficulty] != '0' * difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()
        return block.nonce

    def create_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def get_balance(self, account):
        balance = account.balance
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == account.name:
                    balance -= tx.amount
                if tx.recipient == account.name:
                    balance += tx.amount
        return balance

# Create a blockchain
blockchain = Blockchain()

# Store user accounts in a dictionary
user_accounts = defaultdict(Account)

while True:
    print("\nBlockchain Menu:")
    print("1. Create Account")
    print("2. Make Transaction")
    print("3. Mine Block")
    print("4. Check Balance")
    print("5. Show all the blocks in blockchain")
    print("6. Show all the pending transactions")
    print("7. Exit")

    choice = input("Enter your command number: ")

    if choice == "1":
        # Create an account
        name = input("Enter account name: ")
        user_accounts[name] = Account(name)
        amount = input("Enter amount for balance: ")
        user_accounts[name].deposit(int(amount))
        print(f"Account '{name}' created successfully!")

    elif choice == "2":
        # Make a transaction
        sender_name = input("Enter sender's account name: ")
        recipient_name = input("Enter recipient's account name: ")
        amount = float(input("Enter the amount to send: "))

        sender_account = user_accounts.get(sender_name)
        recipient_account = user_accounts.get(recipient_name)

        if sender_account and recipient_account:
            transaction = Transaction(sender_account, recipient_account, amount)
            blockchain.create_transaction(transaction)
            print("Transaction added to pending transactions.")
        else:
            print("No such sender or recipient, try again!")

    elif choice == "3":
        # Mine a block
        miner_name = input("Enter miner's account name: ")
        miner_account = user_accounts.get(miner_name)

        if miner_account:
            mined_block = blockchain.mine_pending_transactions(miner_account)
            if mined_block:
                print(f"Block #{mined_block.index} mined successfully!")
        else:
            print(f"No miner account named {miner_name}")

    elif choice == "4":
        # Check balance
        account_name = input("Enter account name: ")
        account = user_accounts.get(account_name)

        if account:
            balance = blockchain.get_balance(account)
            print(f"Account balance for '{account_name}': {balance}")
        else:
            print(f"No account named {account_name}")

    elif choice == "5":
        # Show all blocks in the blockchain
        for block in blockchain.chain:
            print(f"\nBlock #{block.index}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Merkle Root: {block.merkle_root}")
            print(f"Nonce: {block.nonce}")
            print(f"Hash: {block.hash}")
            print("Transactions:")
            for transaction in block.transactions:
                print(f"  Sender: {transaction.sender.name}")
                print(f"  Recipient: {transaction.recipient.name}")
                print(f"  Amount: {transaction.amount}")
            print()

    elif choice == "6":
        # Show all pending transactions
        if blockchain.pending_transactions:
            print("Pending Transactions:")
            for transaction in blockchain.pending_transactions:
                print(f"Sender: {transaction.sender.name}")
                print(f"Recipient: {transaction.recipient.name}")
                print(f"Amount: {transaction.amount}")
                print()
        else:
            print("No pending transactions.")

    elif choice == "7":
        # Exit the program
        print("Exiting the Blockchain program.")
        break

    else:
        print("Invalid choice. Please select a valid option.")