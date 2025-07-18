import json

def extract_invoice_data(text: str):
    # Simulated GPT-style output from PDF text
    return {
        "invoice_id": "INV-2024-123",
        "vendor": "ABC Pvt Ltd",
        "date": "2024-07-10",
        "items": [
            {"desc": "Consulting", "amount": 10000, "tds": 1000},
            {"desc": "Hosting", "amount": 5000, "tds": 250}
        ],
        "total": 15000
    }
