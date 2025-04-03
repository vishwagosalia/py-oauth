### **📝 Project Overview**
This is a FastAPI-based authentication project that supports traditional login/logout mechanisms and Google OAuth login. It also includes a weather API, which is restricted to authenticated users. The database used is **PostgreSQL**, running inside a **Podman container**.

---

## ⚙️ **Pre-requisites**
Before running the project, ensure you have the following installed:

1. **Python 3.10+** (Recommended: Python 3.12)
2. **PostgreSQL**
3. **Virtual Environment (venv)**
4. **Libpq (PostgreSQL Client)**
5. **Pip (Python Package Manager)**

---

## 🚀 **Setup & Running the Project**
Follow these steps to set up and run the project:

### **1️⃣ Clone the Repository**
```bash
git clone <repository_url>
cd <repository_name>
```

### **2️⃣ Setup Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Configure Environment Variables**
Export the below variables:
```
export DATABASE_URL=postgresql://user:password@localhost:5432/dbname
export GOOGLE_CLIENT_ID=<your_google_client_id>
export GOOGLE_CLIENT_SECRET=<your_google_client_secret>
```

### **5️⃣ Start PostgreSQL Container (If using Podman)**

### **6️⃣ Run the FastAPI Server**
```bash
uvicorn main:app --reload
```
