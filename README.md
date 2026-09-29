# 🍯 HONEY CHAIN

### Digital Honey Traceability & Verification System

**Smart India Hackathon 2026 – SIH26021**

**Theme:** Agriculture, FoodTech & Rural Development

> **One Batch → One QR → One Verifiable Story**

**GitHub Repository:**
https://github.com/Abhay-Pratap28/Honey-chain-tracker

---

## 📌 Overview

**Honey Chain** is a digital traceability system designed to improve the **transparency, authenticity, and traceability of honey throughout its supply chain**.

The system records important information about a honey batch at every major stage, from harvesting to dispatch, and links these records using a **blockchain-inspired tamper-evident data structure**.

Each honey batch receives a unique identity and can be tracked through the following stages:

**Beekeeper → Harvest → Extraction → Processing → Packaging → Dispatch**

The system generates a QR code associated with the batch identity and verification information, allowing the batch record to be verified digitally.

---

## 🎯 Problem Statement

Honey passes through multiple stages and handlers before reaching the consumer.

During this process, it can be difficult to:

* Identify the original beekeeper or source
* Track the movement of a particular honey batch
* Verify whether recorded information has been modified
* Maintain a reliable history of processing and packaging
* Provide consumers with transparent information about the product
* Detect inconsistencies in supply-chain records

Traditional record-keeping systems may rely heavily on centralized databases or manual documentation, making verification and transparency difficult.

---

## 💡 Our Solution

Honey Chain creates a **digital, tamper-evident history for every honey batch**.

When a batch is registered, its information is recorded digitally. As the batch moves through different stages, a new blockchain record is created and linked to the previous record through cryptographic hashes.

### Core Concept

```text
                    HONEY CHAIN

               🐝 Beekeeper / Farm
                        ↓
                   🌼 Harvest
                        ↓
                  🧪 Extraction
                        ↓
                  ⚙️ Processing
                        ↓
                   📦 Packaging
                        ↓
                   🚚 Dispatch
                        ↓
                 🔐 Verification
                        ↓
                    👤 Consumer
```

Each stage contributes to the batch's digital history.

---

## 🔗 Key Features

### 1. Batch Registration

A new honey batch can be registered using:

* Batch ID
* Beekeeper / Farm
* Harvest Location
* Quantity

Each batch receives a unique identity in the system.

---

### 2. Supply Chain Tracking

The batch can be updated as it moves through different stages:

1. Harvested
2. Extracted
3. Processed
4. Packaged
5. Dispatched

The system maintains the history of these stages.

---

### 3. Blockchain-Based Records

Each stage is stored as a block containing information such as:

* Block index
* Timestamp
* Batch ID
* Stage
* Location
* Handler
* Quality information
* Seal information
* Previous block hash
* Current block hash

The current hash is generated using **SHA-256**.

### Simplified Structure

```text
Block N

│
├── Stage Data
├── Timestamp
├── Previous Hash
└── Current Hash
          ↓
      Block N+1
          │
          ├── Stage Data
          ├── Timestamp
          ├── Previous Hash
          └── Current Hash
```

---

### 4. Tamper Detection

Each block contains the hash of the previous block.

If information inside an earlier block is changed, its calculated hash changes.

This allows the system to detect inconsistencies in the chain.

```text
Original:

Block 1 → Hash A
           ↓
Block 2 → Hash B
           ↓
Block 3 → Hash C


After unauthorized modification:

Block 1 → Hash X ❌
           ↓
Block 2 → Hash B ❌ Previous Hash Mismatch
           ↓
Block 3 → Hash C
```

The system can therefore report the blockchain as:

* **VALID**
* **TAMPERED**

---

### 5. QR Code Generation

A QR code can be generated for a honey batch.

The QR code is associated with the batch identity and verification information.

### Concept

```text
Honey Batch
     ↓
Unique Batch ID
     ↓
QR Code
     ↓
Batch Verification
     ↓
Traceability History
```

This provides a simple way to connect the physical honey product with its digital record.

---

### 6. Batch Verification

The application provides a **Verify Batch** feature.

The user enters a Batch ID and the system checks the corresponding records.

The verification process can show:

* Batch existence
* Blockchain status
* Stage history
* Recorded batch information
* Hash-chain consistency

---

### 7. Blockchain Verification

A dedicated **Verify Blockchain** function checks the integrity of the stored chain.

The system verifies:

* Block hashes
* Previous-hash relationships
* Batch history
* Record consistency

This provides a simple demonstration of blockchain-based integrity checking.

---

## 🖥️ Prototype

Honey Chain is currently implemented as a **desktop prototype**.

### Main Interface

The GUI provides access to:

* **Register Batch**
* **Update Batch**
* **Verify Batch**
* **Track Batch**
* **Verify Blockchain**

The interface is designed to keep the workflow simple enough for demonstration and future adoption.

---

## 🛠️ Technology Stack

| Technology     | Purpose                                |
| -------------- | -------------------------------------- |
| **Python**     | Core application development           |
| **Tkinter**    | Graphical User Interface               |
| **SQLite**     | Local database storage                 |
| **SHA-256**    | Cryptographic hashing                  |
| **QRCode**     | QR code generation                     |
| **JSON**       | Structured data representation         |
| **Git/GitHub** | Version control and project management |

---

## 🏗️ System Architecture

```text
                    USER
                      │
                      ▼
             ┌─────────────────┐
             │   Tkinter GUI   │
             └────────┬────────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
      Register      Update      Verify
       Batch        Batch       Batch
          │           │           │
          └───────────┼───────────┘
                      ▼
             ┌─────────────────┐
             │  Honey Chain    │
             │ Blockchain Logic│
             └────────┬────────┘
                      │
             ┌────────┴────────┐
             ▼                 ▼
       SHA-256 Hashing    QR Generation
             │                 │
             └────────┬────────┘
                      ▼
             ┌─────────────────┐
             │ SQLite Database │
             └─────────────────┘
```

---

## 🗄️ Database Structure

The prototype uses **SQLite** for persistent storage.

### `batches`

Stores the basic information of each honey batch.

| Field       | Description                |
| ----------- | -------------------------- |
| `batch_id`  | Unique batch identifier    |
| `beekeeper` | Beekeeper/Farm information |
| `location`  | Harvest location           |
| `quantity`  | Batch quantity             |

### `blockchain_record`

Stores the traceability history.

| Field         | Description                |
| ------------- | -------------------------- |
| `id`          | Database record ID         |
| `batch_id`    | Associated batch           |
| `stage`       | Supply-chain stage         |
| `location`    | Stage location             |
| `handler`     | Responsible handler        |
| `quality`     | Quality information        |
| `seal_id`     | Packaging/seal information |
| `timestamp`   | Time of record             |
| `prevhash`    | Previous block hash        |
| `hash`        | Current block hash         |
| `block_index` | Block sequence number      |

---

## 🔐 How Blockchain Verification Works

The prototype uses a simplified blockchain structure.

For each block:

```text
Hash =
SHA256(
    Block Index +
    Timestamp +
    Block Data +
    Previous Hash
)
```

The hash is stored with the block.

When verification is performed, the system recalculates the hash and compares it with the stored value.

It also checks whether:

```text
Current Block's Previous Hash
              =
Previous Block's Hash
```

If these conditions are satisfied throughout the batch history, the chain is considered valid.

---

## 🔄 Complete Workflow

```text
START
  │
  ▼
Register Honey Batch
  │
  ▼
Create First Blockchain Record
  │
  ▼
Generate Batch Identity
  │
  ▼
Update Supply Chain Stage
  │
  ├── Extraction
  │
  ├── Processing
  │
  ├── Packaging
  │
  └── Dispatch
  │
  ▼
Create Linked Blockchain Records
  │
  ▼
Generate QR Code
  │
  ▼
Track / Verify Batch
  │
  ▼
Verify Blockchain Integrity
  │
  ▼
VALID / TAMPERED
```

---

## 📱 Example Batch Journey

Suppose a batch has the ID:

```text
HC001
```

Its journey can be represented as:

```text
HC001
 │
 ├── 🌼 Harvested
 │     └── Beekeeper + Location + Quantity
 │
 ├── 🧪 Extracted
 │     └── Extraction details
 │
 ├── ⚙️ Processed
 │     └── Processing information
 │
 ├── 📦 Packaged
 │     └── Packaging / Seal information
 │
 └── 🚚 Dispatched
       └── Dispatch information
```

All stages are connected through the blockchain hash chain.

---

## 👥 Stakeholders

The proposed system can benefit multiple participants in the honey supply chain.

### 🐝 Beekeepers

* Digital batch registration
* Maintain production history
* Improve traceability of harvested honey

### 🏭 Processors

* Record processing activities
* Maintain batch continuity
* Reduce manual record management

### 📦 Packagers

* Associate packaging information with the batch
* Maintain digital batch history

### 🚚 Distributors

* Track dispatched batches
* Maintain supply-chain records

### 🛒 Consumers

* Access the batch identity
* Verify product history
* Improve transparency and trust

### 🏛️ Regulators / Organizations

* Better traceability
* Easier record verification
* Improved supply-chain visibility

---

## 🌱 Impact

Honey Chain aims to contribute to:

* **Supply-chain transparency**
* **Product traceability**
* **Data integrity**
* **Consumer awareness**
* **Digital record keeping**
* **Trust between supply-chain participants**
* **Reduction of manual documentation**

The system can also provide a foundation for future integration with larger agricultural traceability platforms.

---

## 🚀 Future Scope

The current prototype can be extended into a production-ready platform.

Possible improvements include:

* 🌐 Web-based dashboard
* 📱 Android/iOS consumer application
* ☁️ Cloud-based database
* 🔐 Role-based authentication
* ⛓️ Integration with a distributed blockchain network
* 📍 GPS-based location recording
* 📊 Supply-chain analytics dashboard
* 🧪 Digital quality/certification records
* 🔗 API integration with government/agriculture platforms
* 🏷️ Advanced anti-counterfeit product identification
* 🌍 Multi-farm and multi-processing-unit support

---

## ⚙️ Installation

### Prerequisites

Install:

* Python 3.x
* Git
* Required Python packages

### Clone the Repository

```bash
git clone https://github.com/Abhay-Pratap28/Honey-chain-tracker.git
```

Move into the project directory:

```bash
cd Honey-chain-tracker
```

### Install Dependencies

```bash
pip install -r requirements.txt
```
### Run the Application

```bash
python app.py
```

---

## 📁 Project Structure

```text
Honey-chain-tracker/
│
├── app.py
├── honey_chain.py
├── honey_chain_database.db
├── requirements.txt
├── README.md
│
└── QR Codes/
```

> The exact files may vary as the prototype is further developed.

---

## 🧪 Prototype Testing

The prototype can be demonstrated using the following workflow.

### Test 1 – Register Batch

1. Open the application.
2. Select **Register Batch**.
3. Enter batch information.
4. Register the batch.

### Test 2 – Update Batch

1. Enter an existing Batch ID.
2. Select the next supply-chain stage.
3. Enter the required stage information.
4. Save the update.

### Test 3 – Track Batch

1. Enter the Batch ID.
2. Select **Track Batch**.
3. View the complete batch history.

### Test 4 – Verify Blockchain

1. Select **Verify Blockchain**.
2. Choose/enter the required batch.
3. The application checks the hash chain.
4. The result is displayed as **VALID** or **TAMPERED**.

---

## 🔒 Security Concept

Honey Chain uses cryptographic hashing to make unauthorized modification detectable.

The prototype does **not claim that a local SQLite database is itself a decentralized blockchain**.

Instead, the current implementation demonstrates the core concept of:

> **Linked blocks + cryptographic hashes + integrity verification**

A future production implementation can migrate the blockchain layer to a distributed blockchain network.

---

## 🎯 Why Honey Chain?

Honey Chain focuses on solving a practical traceability problem using technologies that can be demonstrated through a working prototype.

The key idea is simple:

```text
Physical Honey
      ↓
Unique Batch Identity
      ↓
Digital Supply Chain Records
      ↓
Linked Hashes
      ↓
QR-Based Access
      ↓
Verification
      ↓
Greater Transparency
```

---

## 🏆 Smart India Hackathon 2026

**Problem Statement:** SIH26021

**Theme:** Agriculture, FoodTech & Rural Development

**Project:** Honey Chain – Digital Honey Traceability & Verification System

### Project Vision

> **To create a transparent and verifiable digital journey for every honey batch — from beekeeper to consumer.**

---

## 👨‍💻 Team

**Team Name:** Team 404 Founders

**Project:** Honey Chain

**Hackathon:** Smart India Hackathon 2026

### Team Members

Add your actual team members here:

| Name               | Role                         |
| -------------      |---------------------------- |
| Yogesh Bagadwal    | Team Lead / Development      |
| Abhay Pratap       | Backend / Blockchain         |
| Karan Dobriyal     | Frontend / GUI               |
| Shubham Kabadwal   | Database / Testing           |
| Anupriya Kweera    | Documentation / Presentation |
| Kamal Singh Mehra  | Research / Development       |

---

## 📄 License

This project is developed as a prototype for **Smart India Hackathon 2026**.

License and open-source terms can be added based on the team's future deployment and repository requirements.

---

## ⭐ Conclusion

Honey Chain demonstrates how **digital traceability, QR-based identification, databases, and cryptographic hash chains** can be combined to create a transparent honey supply-chain system.

The prototype establishes the foundation for a scalable traceability platform that can be expanded beyond honey to other agricultural and food products.

---

# 🍯 One Batch → One QR → One Verifiable Story
