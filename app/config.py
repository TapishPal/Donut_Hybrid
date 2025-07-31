import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# DocVQA Fields
FIELDS = {
    "invoice_number": "What is the invoice number?",
    "invoice_date":   "What is the invoice date?",
    "total_amount":   "What is the total amount?",
    "bill_to": "What is the full name and address under the 'Bill To' or 'Buyer Details' section?"
}

# Model Names
DOCVQA_MODEL = "naver-clova-ix/donut-base-finetuned-docvqa"
CORD_MODEL = "naver-clova-ix/donut-base-finetuned-cord-v2"
