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
        self.merkle_root = self.calculate_merkle_root()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = str(self.index) + self.previous_hash + str(self.timestamp) + str(self.transactions) + str(self.nonce)
        return hashlib.sha256(data.encode()).hexdigest()
    
    def calculate_transaction_hashes(self, transaction_data):
        # Calculate the SHA-256 hash for each transaction data
        return [hashlib.sha256(data.encode()).hexdigest() for data in transaction_data]
    
    def calculate_merkle_root(self):
        # Calculate the Merkle root from the list of transaction data
        transaction_data = [tx.sender + tx.recipient + str(tx.amount) for tx in self.transactions]
        transaction_hashes = self.calculate_transaction_hashes(transaction_data)
        
        # Check if there are no transactions (empty block)
        if not transaction_hashes:
            return "0"
        
        while len(transaction_hashes) > 1:
            next_level = []
            for i in range(0, len(transaction_hashes), 2):
                hash_pair = transaction_hashes[i] + (transaction_hashes[i+1] if i+1 < len(transaction_hashes) else transaction_hashes[i])
                next_level.append(hashlib.sha256(hash_pair.encode()).hexdigest())
            transaction_hashes = next_level
        return transaction_hashes[0]
    
    def is_valid(self):
        # Check if the block's hash starts with a given number of leading zeros (proof-of-work)
        difficulty = 2  # Adjust as needed
        if self.hash[:difficulty] != '0' * difficulty:
            return False

        # Check if the Merkle root matches the calculated Merkle root
        if self.merkle_root != self.calculate_merkle_root():
            return False

        return True

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
        
        # Check if the new block is valid before adding it to the chain
        if new_block.is_valid():
            self.chain.append(new_block)
            print(f"Block #{new_block.index} has been mined and added to the chain!")
            return new_block
        else:
            print("Invalid block! Block was not added to the chain.")
            return None

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

my_blockchain = Blockchain()

# Create some transactions
tx1 = Transaction("Alice", "Bob", 10)
tx2 = Transaction("Bob", "Charlie", 5)
tx3 = Transaction("Alice", "Charlie", 3)

# Add transactions to the pending transaction pool
my_blockchain.create_transaction(tx1)
my_blockchain.create_transaction(tx2)
my_blockchain.create_transaction(tx3)

# Mine a new block to include these transactions
my_blockchain.mine_pending_transactions("Miner")

# Check balances
print("Alice's balance:", my_blockchain.get_balance("Alice"))
print("Bob's balance:", my_blockchain.get_balance("Bob"))
print("Charlie's balance:", my_blockchain.get_balance("Charlie"))
print("Miner's balance:", my_blockchain.get_balance("Miner"))