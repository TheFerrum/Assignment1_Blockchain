import hashlib
import time

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = str(self.index) + self.previous_hash + str(self.timestamp) + str(self.transactions) + str(self.nonce)
        return hashlib.sha256(data.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []

    def create_genesis_block(self):
        return Block(0, "0", int(time.time()), [],0)

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)
    
    def mine_pending_transactions(self, miner_address):
        reward_transaction = Transaction("Blockchain Reward", miner_address, 0.01)
        self.pending_transactions.append(reward_transaction)

        new_block = Block(len(self.chain), self.get_latest_block().hash, int(time.time()), self.pending_transactions)
        self.pending_transactions = []  # Clear pending transactions
        new_block.nonce = self.proof_of_work(new_block)
        self.chain.append(new_block)
        print(f"Block #{new_block.index} has been mined!")
        return new_block

    def proof_of_work(self, block, difficulty=2):
        while block.hash[:difficulty] != '0' * difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()
        return block.nonce

    def create_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == address:
                    balance -= tx.amount
                if tx.recipient == address:
                    balance += tx.amount
        return balance

# Create a blockchain
my_blockchain = Blockchain()

# Add blocks to the blockchain
block1 = Block(1, my_blockchain.get_latest_block().hash, int(time.time()), "Data 1")
my_blockchain.add_block(block1)

block2 = Block(2, my_blockchain.get_latest_block().hash, int(time.time()), "Data 2")
my_blockchain.add_block(block2)

# Print the blockchain
for block in my_blockchain.chain:
    print(f"Block {block.index} - Hash: {block.hash}")

my_blockchain2 = Blockchain()

# Create some transactions
tx1 = Transaction("Alice", "Bob", 10)
tx2 = Transaction("Bob", "Charlie", 5)
tx3 = Transaction("Alice", "Charlie", 3)

# Add transactions to the pending transaction pool
my_blockchain2.create_transaction(tx1)
my_blockchain2.create_transaction(tx2)
my_blockchain2.create_transaction(tx3)

# Mine a new block to include these transactions
my_blockchain2.mine_pending_transactions("Miner")

# Check balances
print("Alice's balance:", my_blockchain2.get_balance("Alice"))
print("Bob's balance:", my_blockchain2.get_balance("Bob"))
print("Charlie's balance:", my_blockchain2.get_balance("Charlie"))
print("Miner's balance:", my_blockchain2.get_balance("Miner"))