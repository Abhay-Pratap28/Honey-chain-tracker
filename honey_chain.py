# To create a Honey chain tracking system using Blockchain 
# technology

import hashlib
import json
from datetime import datetime

# Creating Block

class Block:

    def __init__(self , index , data , prevhash ):
        self.index = index
        self.timestamp = str(datetime.now())
        self.data = data
        self.prevhash = prevhash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_data = (
            str(self.index)
            + self.timestamp
            + json.dumps(self.data , sort_keys= True)
            + self.prevhash
        )

        return hashlib.sha256(block_data.encode()).hexdigest()


# Create Blockchain

class Blockchain:

    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(
            0,
            {"Message":"create genesis block"},
            "0"
        )

    def add_block(self , data):
        prev_block = self.chain[-1]

        new_block = Block(
            len(self.chain),
            data ,
            prev_block.hash
        )

        self.chain.append(new_block)

    def is_valid(self):

        for i in range( 1, len(self.chain)):

            current = self.chain[i]
            previous = self.chain[i-1]

            if current.hash != current.calculate_hash():
                return False

            if current.prevhash != previous.hash:
                return False

        return True


    # Create blockchain
honey_chain = Blockchain()

# Add honey records
honey_chain.add_block({
    "batch_id": "HC001",
    "stage": "Harvested",
    "location": "Uttarakhand",
    "quantity": "50 kg"
})

honey_chain.add_block({
    "batch_id": "HC001",
    "stage": "Processed",
    "location": "Processing Unit"
})

honey_chain.add_block({
    "batch_id": "HC001",
    "stage": "Bottled",
    "quantity": "500 bottles"
})

# Display blockchain
for block in honey_chain.chain:

    print("\n-----------------------")
    print("Block:", block.index)
    print("Data:", block.data)
    print("Previous Hash:", block.prevhash)
    print("Hash:", block.hash)


print("\nBlockchain valid:", honey_chain.is_valid())

honey_chain.chain[1].data = {
    "batch_id": "HC001",
    "stage": "Harvested",
    "location": "Uttarakhand",
    "quantity": "100 kg"
}

print("\nBlockchain valid:", honey_chain.is_valid())
        
        
        

    
