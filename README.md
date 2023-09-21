# Assignment1_Blockchain
Assignment 1 of Blockchain

1.0 Investigate Blockchain Principles (5 points):

Blockchain has five elements: Distribution, encryption, immutability, tokenization and decentralization.

**Distribution**: Participants in a blockchain are physically separated from one another but are linked through a network. Each user running a full node has an up-to-date copy of a ledger that is updated as new transactions are made.
  
**Encryption**: Blockchain employs public and private keys and other technologies to securely and semi-anonymously store data in the blocks (participants use pseudonyms). Participants can keep their identities and other personal information private and only divulge the information required for the transaction.
  
  **Immutability**: Completed transactions are time-stamped, cryptographically signed, and added one at a time to the ledger. Records cannot be altered or corrupted unless all parties agree that it is necessary to do so. 
  
  **Tokenization**: In a blockchain, value is securely exchanged during transactions and other interactions. Tokens are used to represent value, which can be anything from data to physical assets to financial assets. Tokens also give users the ability to manage their personal data, which is a key component of the blockchain's business case.
  
  **Decentralization**: Due to a consensus mechanism, nodes in the distributed network are responsible for maintaining both network data and the rules that govern how the network functions. Decentralization actually refers to the fact that no single organization is in charge of all the computers, information, or rules. 


3.1 Define Blockchain Structure (10 points):
	
 **Header**: In the entire blockchain, the header is used to identify the specific block. It manages every blockchain block. As part of routine mining operations, miners routinely hash a block header by altering the nonce value. The block header contains three kinds of block metadata.
  
  **Previous Block Address/ Hash**: The i+1th block is linked to the ith block using the hash using the previous block address. It is, in essence, a reference to the hash of the chain's previous (parent) block.
  
  **Timestamp**: A technique called a timestamp verifies the data in a block and gives digital documents a creation date or time. The document or event's timestamp is a string of characters that both uniquely identifies it and shows when it was created.
  
  **Nonce**: Central to the block's proof of work is a nonce number that is only ever used once. If it is less than or equal to the current target, it is compared to the live target. People who mine, test, and remove a large number of once every second until they discover a legitimate instance of a valuable once.
  
  **Merkle Root**: A frame of various data blocks called a Merkle Root is a sort of data structure. A Merkle Tree creates a digital fingerprint of each transaction and saves them all together in a block. It enables users to confirm if a transaction may or cannot be included in a block.


![Structureofblocksinblockchain](https://github.com/TheFerrum/Assignment1_Blockchain/assets/90481840/be9e4815-7835-47f3-928d-d2f1deebc298)


                                                    Figure from geeksforgeeks.org

The Genesis Block, sometimes referred to as Block 0, is the initial block in a blockchain, and it is where all subsequent blocks are added. Since each block refers the one before it, it serves as the ancestor to which all other blocks can trace their descent.


