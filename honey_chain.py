# To create a Honey chain tracking system using Blockchain 
# technology

import hashlib
import json
from datetime import datetime
import qrcode
import sqlite3

conn =sqlite3.connect("honey_chain_database.db")
cursor  = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS batches(
    batch_id TEXT PRIMARY KEY,
    beekeeper TEXT,
    location TEXT,
    quantity TEXT)
    """)

cursor.execute("""
CREATE TABLE IF NOT EXISTS blockchain_record(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id TEXT,
    stage TEXT,
    location TEXT,
    handler TEXT,
    quality TEXT,
    seal_id TEXT,
    timestamp TEXT,
    prevhash TEXT,
    hash TEXT
)
""")

conn.commit()

try:
    cursor.execute(
        "ALTER TABLE blockchain_record ADD COLUMN block_index INTEGER"
    )
    conn.commit()
except sqlite3.OperationalError:
    pass

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

       cursor.execute(""" SELECT batch_id , beekeeper, location , quantity
        from BATCHES WHERE batch_id = ?
        """,(batch_id,))

       batch = cursor.fetchone()

       if not batch :
           return []

       harvested_data = {
           "batch_id" : batch[0],
           "stage" : "harvested",
           "beekeeper" : batch[1],
           "location" : batch[2],
           "quantity" : batch[3]
       }

       history = []

       harvested_block = Block(
           1 , harvested_data , "0"
       )

       history.append(harvested_block)

       cursor.execute("""
        Select stage , location , handler , quality , seal_id,
        timestamp , prevhash , hash , block_index
        from blockchain_record 
        where batch_id = ?""",(batch_id,))

       records = cursor.fetchall()

       for index, record in enumerate(records, start=2):
            
           
            data = { "batch_id": batch_id, 
                   "stage": record[0], 
                   "location": record[1], 
                   "handler": record[2], 
                   "quality": record[3], 
                   "seal_id": record[4] 
                   }

            block = Block(
               record[8] , data , record[6]
           )

            block.timestamp = record[5]
            block.hash = record[7] 
            history.append(block) 

       return history


    def register_batch(self , batch_id , beekeeper , location , quantity ):

        if self.find_batch(batch_id):
            print("\n Batch alredy exists")
            return

        data = {
            "batch_id" : batch_id,
            "stage"    : "harvested",
            "beekeeper" : beekeeper,
            "location" : location,
            "quantity" : quantity
        }

        block = Block(1, data, "0")

        cursor.execute("""
        INSERT INTO BATCHES (batch_id , beekeeper , location , quantity )
        VALUES( ? , ? , ? ,? )
        """,(
            batch_id , beekeeper , location , quantity
        ))

        cursor.execute("""
        INSERT INTO blockchain_record (
            batch_id, stage, location, handler, quality, seal_id,
            timestamp, prevhash, hash, block_index
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            batch_id,
            "harvested",
            location,
            None,
            None,
            None,
            block.timestamp,
            block.prevhash,
            block.hash,
            block.index
        ))

        conn.commit()

        print("\nBatch registered succesfully")

    def update_batch(self , batch_id , stage , location = None , handler = None , 
                     quality = None , seal_id = None):

        history = self.find_batch(batch_id)

        if not history :
            print("Batch not found !")
            return

        current_stage = history[-1].data["stage"]

        stages = ["harvested", "extracted", "processed", "packaged", "dispatched"]

        stage = stage.lower()

        if stage not in stages:
            print("Invalid stage!")
            print("Use: extracted, processed, packaged or dispatched")
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
            "location" : location , 
            "handler"  : handler ,
            "quality"  : quality , 
            "seal_id"  : seal_id
            }


        self.add_block(data) 

        block = self.chain[-1]

        cursor.execute("""
        INSERT INTO blockchain_record (batch_id, stage, location, handler, quality, seal_id,
        timestamp, prevhash, hash , block_index)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ? , ?)
        """, (
            batch_id,
            stage,
            location,
            handler,
            quality,
            seal_id,
            block.timestamp,
            block.prevhash,
            block.hash,
            block.index
        ))

        conn.commit()

        print("\nBatch updated succesfully")

        generate_qr(batch_id)

    def load_batch_from_database(self, batch_id):

        cursor.execute("""
            SELECT batch_id, beekeeper, location, quantity
            FROM batches
            WHERE batch_id = ?
        """, (batch_id,))

        batch = cursor.fetchone()

        if not batch:
            return []

        cursor.execute("""
            SELECT stage, location, handler, quality, seal_id,
                timestamp, prevhash, hash, block_index
            FROM blockchain_record
            WHERE batch_id = ?
            ORDER BY block_index
        """, (batch_id,))

        records = cursor.fetchall()

        history = []

        for record in records:

            stage = record[0]

            if stage == "harvested":

                data = {
                    "batch_id": batch[0],
                    "stage": "harvested",
                    "beekeeper": batch[1],
                    "location": batch[2],
                    "quantity": batch[3]
                }

            else:

                data = {
                    "batch_id": batch_id,
                    "stage": stage,
                    "location": record[1],
                    "handler": record[2],
                    "quality": record[3],
                    "seal_id": record[4]
                }

            block = Block(
                record[8],
                data,
                record[6]
            )

            block.timestamp = record[5]
            block.hash = record[7]

            history.append(block)

        return history

                
    def is_valid(self, batch_id):

        history = self.load_batch_from_database(batch_id)

        if not history:
            return False

        # Check every block's own hash
        for i in range(len(history)):

            current = history[i]

            # Check whether the block data has been changed
            if current.hash != current.calculate_hash():
                return False

            # First block must point to "0"
            if i == 0:

                if current.prevhash != "0":
                    return False

            # Every other block must point to the previous block
            else:

                previous = history[i - 1]

                if current.prevhash != previous.hash:
                    return False

        return True


    # Create blockchain
honey_chain = Blockchain()


def generate_qr(batch_id):

    history = honey_chain.find_batch(batch_id)

    if not history:
        print("\n❌ Batch not found")
        return

    first_record = history[0].data

    qr_data = ""

    qr_data += "HONEY CHAIN - TRACEABILITY\n"
    qr_data += "==============================\n"

    qr_data += "BATCH INFORMATION\n"
    qr_data += "Batch ID  : " + batch_id + "\n"
    qr_data += "Beekeeper : " + str(first_record.get("beekeeper")) + "\n"
    qr_data += "Quantity  : " + str(first_record.get("quantity")) + "\n"
    qr_data += "Harvest Location : " + str(first_record.get("location")) + "\n"

    qr_data += "\nSUPPLY CHAIN JOURNEY\n"
    qr_data += "==============================\n"

    for i, block in enumerate(history, start=1):

        record = block.data

        qr_data += "\nSTEP " + str(i) + "\n"
        qr_data += "Stage    : " + str(record.get("stage")) + "\n"
        qr_data += "Location : " + str(record.get("location")) + "\n"

        if record.get("handler"):
            qr_data += "Handler  : " + str(record.get("handler", "N/A")) + "\n"

        if record.get("quality"):
            qr_data += "Quality  : " + str(record.get("quality")) + "\n"

        if record.get("seal_id"):
            qr_data += "Seal ID  : " + str(record.get("seal_id")) + "\n"

        qr_data += "Time     : " + str(block.timestamp) + "\n"

    qr_data += "\n==============================\n"
    qr_data += "BLOCKCHAIN VERIFICATION\n"
    qr_data += "Status: "

    if honey_chain.is_valid( batch_id):
        qr_data += "VALID\n"
    else:
        qr_data += "TAMPERED\n"

    qr_data += "==============================\n"

    qr = qrcode.make(qr_data)

    filename = batch_id + "_QR.png"

    qr.save(filename)

    print("\n✅ QR Generated:", filename)

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
    print("Beekeeper :", first_record.data.get("beekeeper"))
    print("Location  :", first_record.data.get("location"))
    print("Quantity  :", first_record.data.get("quantity"))
    print("Time      :", first_record.timestamp)

    print("\n----- Supply Chain History -----")

    history = history[1::]

    for i , block in enumerate(history , start =1):

        record = block.data

        print("Step     :", i)
        print("stage    :", record.get("stage"))
        print("Location :", record.get("location"))
        print("Handler  :", record.get("handler"))

        if record.get("quality"):
            print("Quality  :", record.get("quality"))

        if record.get("seal_id"):
                    print("Seal ID  :", record.get("seal_id"))

        print("Time     :", block.timestamp)
        print("\n================================")

    print("\n================================")

    if blockchain.is_valid(batch_id): 
            print("Blockchain Status : ✅ VALID")
    else:
            print("Blockchain Status : ⚠️ TAMPERED")

    print("================================")

    

def tamper_test(blockchain):

    print("\n========== TAMPER TEST ==========")

    batch_id = input("Enter Batch ID: ").strip()

    history = blockchain.load_batch_from_database(batch_id)

    if not history:
        print("Batch not found!")
        return

    print("Changing quantity inside the database...")

    cursor.execute("""
        UPDATE batches
        SET quantity = ?
        WHERE batch_id = ?
    """, ("1000 kg", batch_id))

    conn.commit()

    # Check blockchain
    if blockchain.is_valid(batch_id):
        print("Blockchain is VALID")
    else:
        print("WARNING: Blockchain has been TAMPERED!")


def view_database():

    print("\n========== BATCH DATABASE ==========")

    cursor.execute("SELECT * FROM batches")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    print("\n====== BLOCKCHAIN RECORDS ======")

    cursor.execute("""
        SELECT batch_id, stage, location, handler,
               quality, seal_id, timestamp
        FROM blockchain_record
    """)

    records = cursor.fetchall()

    for record in records:
        print(record)

    print("====================================")

# generate_qr("HC001")
# scan_qr("HC001")

# Creating menu

if __name__ == "__main__":

    while True:

        print("\n=========Honey Tracebility System===========")
        print("1. Register Batch")
        print("2. Update Batch")
        print("3. Verify Batch")
        print("4. Check Blockchain")
        print("5. Temper test")
        print("6. View database")
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


        elif (choice == 2):

            batch_id = input("Enter Batch ID: ")
            stage = input("Enter new stage: ")
            location = input("Enter current location: ")
            handler = input("Enter Handler/Unit Name: ")

            if stage.lower() == "processed":
                quality = input("Enter Quality/Test Status: ")

            else:
                quality = None

            if stage.lower() == "packaged":
                seal_id = input("Enter seal_id: ")
            
            else:
                seal_id = None

            honey_chain.update_batch(
                batch_id, stage, location, handler, quality , seal_id
            )

        elif (choice == 3):

            batch_id = input("Ener batch id :")

            verify_batch(
                honey_chain , batch_id
            )

        elif (choice == 4):

            batch_id = input("Enter batch Id : ")

            if (honey_chain.is_valid(batch_id)):
                print("\nBlockchain is valid.")

            else:
                print("\nBlockchain has been tempered ! ")

        elif (choice == 5):

            tamper_test(honey_chain)


        elif (choice == 6):
        
                view_database()
        
        elif (choice == 7):
        
            print("\nThankyou for using Honey Tracebility System")
            break

        else:

            print("Invalid choice")

        
