from fastapi import FastAPI, UploadFile, File, Request
from agents.invoice_reader import extract_invoice_data
from agents.tds_validator import validate_tds
from agents.vendor_reply import generate_reply
from agents.duplicate_checker import check_duplicate
from agents.tds_categorizer_llm import auto_categorize_tds_llm
from fastapi import UploadFile, File

app = FastAPI()

@app.post("/read-invoice")
async def read_invoice(file: UploadFile = File(...)):
    content = await file.read()
    return extract_invoice_data(content.decode())

@app.post("/validate-tds")
def tds_validator(invoice: dict):
    items = invoice["tds_categorization"]["tds_categorization"]

    validated = []

    for item in items:
        result = validate_tds(
            item_text=item["item"],
            predicted_category=item["category"],
            predicted_rate=str(item["tds_rate"]).strip()
        )
        validated.append(result)

    return {"validated_results": validated}

@app.post("/vendor-reply")
def vendor_reply(invoice: dict):
    return generate_reply(invoice)

@app.post("/check-duplicate")
def duplicate(invoice: dict):
    return check_duplicate(invoice)


@app.post("/auto-categorize-tds-llm")
async def categorize_tds_using_llm(file: UploadFile = File(...)):
    if not file.filename.endswith(".txt"):
        return {"error": "Only .txt files are supported."}

    content = await file.read()
    try:
        text = content.decode()
        result = auto_categorize_tds_llm(text)
        return {"tds_categorization": result}
    except Exception as e:
        return {"error": str(e)}