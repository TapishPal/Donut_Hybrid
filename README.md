# 🧾 Donut-Based Invoice OCR Tool

This project is a hybrid **Invoice OCR Automation Tool** that uses advanced document understanding models to extract structured data from invoice documents. The backend is built with **FastAPI**, and the system integrates OCR-free document models like **Donut**, along with hybrid approaches using datasets like **DocVQA** and **CORD-v2** for enhanced accuracy.

---

## 🧠 Project Highlights

- 🔍 **Donut (Document Understanding Transformer)** — A transformer-based, OCR-free model developed by Samsung for deep document understanding.
- ❓ **DocVQA (Document Visual Question Answering)** — A benchmark dataset designed to answer questions based on visually rich documents.
- 🧾 **CORD-v2 (Consolidated Receipt Dataset v2)** — An annotated dataset of receipt-style documents that helps train models for key-value and table extraction.

This hybrid architecture provides powerful information extraction from invoices, bypassing traditional OCR limitations.

---

## ⚙️ Setup Instructions

After cloning, or downloading zip from the repo, open the folder in VS code (or any editor). You also need to have Anaconda Navigator, since used conda command to create the environment with python 3.10 version.

### 1️⃣ Create a Conda Environment (Python 3.10)

```bash
conda create -n invoice-env python=3.10
conda activate invoice-env
```

### 2️⃣ Install Required Packages

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the FastAPI Server

```bash
uvicorn main:app --reload
```

### 4️⃣ Open in Browser

Go to:

```
http://127.0.0.1:8000/docs
```

You will see the FastAPI Swagger UI where you can test the API endpoints.

---

## 🧪 How to Use

1. **Upload your invoice image** using the `/upload` endpoint.
2. **Wait a few moments** while the Donut model processes the document (especially the first time).
3. **View extracted results** such as:
   - Invoice number
   - Vendor details
   - Line items
   - Totals and taxes
4. Results are shown as structured JSON.

---

## 📁 Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── model/
│   ├── services/
│   └── utils/
├── frontend/
│   └── streamlit_app.py
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```



