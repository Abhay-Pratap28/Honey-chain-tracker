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

        history = self.find_batch(batch_id)

        if not history :
            print("Batch not found !")
            return

        current_stage = history[-1]["stage"]

        stages = ["harvested", "processed", "bottled", "distributed"]

        stage = stage.lower()

        if stage not in stages:
            print("Invalid stage!")
            print("Use: processed, bottled or distributed")
            return

        current_index = stages.index(current_stage.lower())

        new_index = stages.index(stage)

        if (new_index <= current_index):
            print("\nInvalid stage transition!")
            print("Current stage:", current_stage)
            print("Cannot move to:", stage)
            return

        if new_index != current_index + 1:
            print("\nInvalid stage transition!")
            print("Next allowed stage:", stages[current_index + 1])
            return

        data={
            "batch_id" : batch_id,
            "stage"    : stage,
            "location" : location
            }


        self.add_block(data) 

        print("\nBatch updated succesfully")
                
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


def generate_qr(batch_id):

    history = honey_chain.find_batch(batch_id)
    
    if not history:
        print("\n❌Batch not found")
        return

    qr_data = "Honeytrace ://" + batch_id

    qr = qrcode.make(qr_data)

    filename = batch_id + "_QR.png"
    qr.save(filename)

    print("QR Generated = " , filename)
    print("QR Data =" , qr_data)


def verify_batch(blockchain , batch_id):


    history = blockchain.find_batch(batch_id)

    if not history:
        print("Batch not found")
        return 

    print("\n================================")
    print("        HONEY BATCH")
    print("================================")

    first_record = history[0]

    print("Batch_id  :" , batch_id)
    print("Beekeeper :", first_record.get("beekeeper"))
    print("Quantity  : ", first_record.get("quantity"))

    print("\n----- Supply Chain History -----")

    for i , record in enumerate(history , start =1):

        print("Step     :", i)
        print("stage    :", record.get("stage"))
        print("Location :", record.get("location"))
        print("\n================================")

    print("\n================================")

    if blockchain.is_valid():
            print("Blockchain Status : ✅ VALID")
    else:
            print("Blockchain Status : ⚠️ TAMPERED")

    print("================================")

    

def tamper_test(blockchain):

    print("\n========== TAMPER TEST ==========")

    if len(blockchain.chain) <= 1:
        print("No batch data available!")
        return

    print("Changing data inside Block 1...")

    # Tamper with the stored data
    blockchain.chain[1].data["quantity"] = "1000 kg"

    # Check blockchain
    if blockchain.is_valid():
        print("Blockchain is VALID")
    else:
        print("WARNING: Blockchain has been TAMPERED!")

def scan_qr(qr_data):

    print("\n========== QR SCAN ==========")
    print("QR Data:", qr_data)

    if not qr_data.startswith("Honeytrace ://"):
        print("❌ Invalid QR code!")
        return

    batch_id = qr_data.replace("Honeytrace ://" , "")

    print("Batch ID =" , batch_id)

    verify_batch(honey_chain , batch_id)

          

# generate_qr("HC001")
# scan_qr("HC001")

# Creating menu

while True:

    print("\n=========Honey Tracebility System===========")
    print("1. Register Batch")
    print("2. Update Batch")
    print("3. Verify Batch")
    print("4. Generate QR")
    print("5. Check Blockchain")
    print("6. Temper test")
    print("7. Exit")

    choice = int(input("Enter Choice:"))

    if (choice == 1):

        batch_id = input("Enter Batch ID: ")
        beekeeper = input("Enter Beekeeper/Farm name: ")
        location = input("Enter Harvest Location: ")
        quantity = input("Enter Quantity: ")

        honey_chain.register_batch(
            batch_id, beekeeper , location , quantity
        )

        print("\nBatch registered succesfully")

    elif (choice == 2):

        batch_id = input("Enter Batch ID: ")
        stage = input("Enter new stage: ")
        location = input("Enter current location: ")

        honey_chain.update_batch(
            batch_id , stage , location
        )

    elif (choice == 3):

        batch_id = input("Ener batch id :")

        verify_batch(
            honey_chain , batch_id
        )

    elif (choice == 4):

        batch_id = input("Enter batch id")

        history = honey_chain.find_batch(batch_id)

        if not history:
            print("\n❌Batch not found")

        else:
            generate_qr(batch_id)

    elif (choice == 5):

        if (honey_chain.is_valid()):
            print("\nBlockchain is valid.")

        else:
            print("\nBlocchain has been tempered ! ")

    elif (choice == 6):

        tamper_test(honey_chain)

    elif (choice == 7):
    
        print("\nThankyou for using Honey Tracebility System")
        break

    else:

        print("Invalid choice")

    
