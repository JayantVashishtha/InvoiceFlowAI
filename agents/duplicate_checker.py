invoices_db = {"INV-2024-100", "INV-2024-101", "INV-2024-123"}

def check_duplicate(invoice: dict):
    if invoice["invoice_id"] in invoices_db:
        return {"duplicate": True, "message": "Invoice already exists"}
    return {"duplicate": False}
