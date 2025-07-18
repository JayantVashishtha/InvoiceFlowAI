def generate_reply(invoice: dict):
    vendor = invoice.get("vendor", "Vendor")
    invoice_id = invoice.get("invoice_id", "Unknown")
    return {
        "to": f"{vendor}@email.com",
        "subject": "Invoice Received",
        "body": f"Hi {vendor},\n\nWe have received invoice {invoice_id}. It's under review.\n\nRegards,\nFinance Team"
    }