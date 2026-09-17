# To create a Honey chain tracking system using Blockchain 
# technology

import hashlib
import json
from datetime import datetime
import qrcode



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

    def find_batch(self , batch_id):

        result = []

        for block in self.chain:

            if( batch_id == block.data.get("batch_id")):
                result.append(block.data)

        return result

    def register_batch(self , batch_id , beekeeper , location , quantity ):

        data = {
            "batch_id" : batch_id,
            "stage"    : "harvested",
            "beekeeper" : beekeeper,
            "location" : location,
            "quantity" : quantity
        }

        self.add_block(data)

    def update_batch(self , batch_id , stage , location = None):

        data={
            "batch_id" : batch_id,
            "stage"    : stage,
            "location" : location
            }


        self.add_block(data) 
                
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

honey_chain.register_batch(
    "HC001" , "ABC Farm" , "uttarakhand" , "50 kg"
)

honey_chain.update_batch(
    "HC001" , "Proccesed" , "Processing unit"
)

honey_chain.update_batch(
    "HC001" , "Botteled" , "Botteling unit"
)

honey_chain.update_batch(
    "HC001" , "Distributed" , "Dehradun"
)



def generate_qr(batch_id):
    qr = qrcode.make(batch_id)
    filename = batch_id + "_QR.png"
    qr.save(filename)

    print("QR Generated = " , filename)
    print("QR contains batch_id =" , batch_id)


def verify_batch(blockcahin , batch_id):

    history = blockcahin.find_batch(batch_id)

    if not history:
        print("Batch not found")
        return 

    print("\n--------------Honey Batch-----------")

    for record in history:
        print("Stage = " , record.get("stage"))

        if "beekeeper" in record:
            print("Beekeeper:", record["beekeeper"])

        if "location" in record:
            print("Location:", record["location"])

        if "quantity" in record:
            print("Quantity:", record["quantity"])

        print("-------------------------------")

def scan_qr(batch_id):
          print("\nQR Scanned")
          print("Batch_Id =", batch_id)
          verify_batch(honey_chain, batch_id)

generate_qr("HC001")
scan_qr("HC001")