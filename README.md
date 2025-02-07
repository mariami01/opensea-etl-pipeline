# OpenSea ETL Pipeline

## About This Project
This project is an **ETL (Extract, Transform, Load) pipeline** that extracts **NFT collection data** from the **OpenSea API**, cleans and transforms the data, and stores it in an SQLite database. 

## Features
- **Extracts NFT collection data** from OpenSea API (Ethereum collections).
- **Transforms and cleans the data**, handling missing values and standardizing formats.
- **Saves raw JSON data** in a `data/` directory.
- **Loads structured data** into an SQLite database using SQLAlchemy ORM.

---

## 📦 Installation & Setup
### **1️⃣ Clone This Repository**
```sh
git clone https://github.com/mariami01/opensea-etl-pipeline.git
cd opensea-etl-pipeline

### **2️⃣ Set Up a Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate     # On Windows

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt

### **4️⃣ Set Up Your OpenSea API Key**
1. Request an API key from OpenSea: OpenSea API Keys
2. Create a .env file in the project root:
```sh
OPENSEA_API_KEY=your_api_key_here

### **Running the ETL Pipeline**
To run the pipeline and fetch OpenSea collections, execute:
python main.py