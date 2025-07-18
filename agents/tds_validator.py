from agents.tds_rules import TDS_RULES

CATEGORY_MAP = {
    # Salary
    "Income Tax": "Salary",
    "Income from Salary": "Salary",
    "Salary Payment": "Salary",
    "Salary": "Salary",

    # Interest
    "Interest": "Interest from Bank/Post Office",
    "Bank Interest": "Interest from Bank/Post Office",
    "Bank interest": "Interest from Bank/Post Office",
    "Interest on Corporate Debentures": "Interest on Securities",
    "Interest on corporate debentures": "Interest on Securities",
    "Income on securities": "Interest on Securities",
    "Income from other sources": "Interest from Bank/Post Office",
    "Income from Other Sources": "Interest from Bank/Post Office",
    "Income on Interest": "Interest from Bank/Post Office",

    # Dividend
    "Income": "Dividend",
    "Dividend": "Dividend",
    "Dividends": "Dividend",
    "Dividend from equity shares": "Dividend",

    # Lottery
    "Lottery Winnings": "Winnings from Lottery/Game Show",
    "Lottery winnings": "Winnings from Lottery/Game Show",
    "Winnings from lottery": "Winnings from Lottery/Game Show",

    # Life Insurance
    "Income on Life Insurance Maturity or Death Claim": "Life Insurance Maturity",
    "Life Insurance Maturity": "Life Insurance Maturity",

    # Mutual Fund
    "MF Unit Repurchase": "Mutual Fund (Non-Equity)",
    "Income on units of mutual fund (other than equity oriented fund)": "Mutual Fund (Non-Equity)",
    "Income on units of mutual fund": "Mutual Fund (Non-Equity)",
    "Income on mutual fund units (units sold or redeemed by a resident individual)": "Mutual Fund (Non-Equity)",

    # Rent
    "Income on Rent": "Rent",
    "Rent for Office Premises": "Rent",
    "Rent for Office Building": "Rent",
    "Rent for Plant & Machinery": "Rent",
    "Rent for Machinery": "Rent",
    "rent for machinery": "Rent",
    "rent for office building": "Rent",
    "Office Space Rent": "Rent",
    "Office Rent": "Rent",
    "Rent for Office": "Rent",

    # Rent by Individual
    "Income from House property": "Rent by Individual",
    "Rent Paid by Individual (>50K/month)": "Rent by Individual",

    # Property Sale
    "Income from House Property": "Rent by Individual",
    "Income from house property or capital gains": "Property Sale",
    "Income from house property or capital gain": "Property Sale",
    "Property Purchase from Seller": "Property Sale",
    "Property Purchase": "Property Sale",
    "Landowner Share under JDA": "Landowner Share under JDA",
    "Landowner share under JDA": "Landowner Share under JDA",

    # Compensation
    "Land Acquisition Compensation": "Compensation on Land Acquisition",

    # Professional/Technical
    "Professional or technical services": "Professional or Technical Services",
    "Professional/Technical Services": "Professional or Technical Services",
    "Google Ad Spend (Advance)": "Professional or Technical Services",
    "Professional Services": "Professional or Technical Services",
    "Freelance/Consultancy Work": "Professional or Technical Services",
    "Legal Consultancy Services": "Professional or Technical Services",
    "Legal Advisory Fees": "Professional or Technical Services",
    "Contract Labour Supply": "Professional or Technical Services",
    "Technical Support Services": "Professional or Technical Services",
    "Technical Support Subscription": "Professional or Technical Services",
    "Payment to Freelancer for Design": "Professional or Technical Services",
    "Annual Maintenance Contract": "Professional or Technical Services",
    "Advertising Charges": "Professional or Technical Services",
    "Website Hosting Services": "Professional or Technical Services",
    "Service for hosting or maintenance of website": "Professional or Technical Services",
    "Service for website hosting is a taxable service under Section 66E of the Finance Act 1994, and TDS is applicable at the rate of 10% as per Section 194C of the Income Tax Act 1961.": "Professional or Technical Services",
    "Services": "Professional or Technical Services",
    "Service Tax": "Professional or Technical Services",

    # Foreign Services
    "Professional or technical services (to a non-resident under section 195)": "Technical Services to Non-Resident",
    "Payment to Foreign Consultant": "Technical Services to Non-Resident",
    "Payment to Non-Resident Entertainer": "Non-Resident Entertainer",

    # FII
    "Income from securities to a Foreign Institutional Investor (FII)": "Income to FII",
    "Income to FII": "Income to FII",

    # Cash Withdrawal
    "Cash Withdrawal above 1 crore": "Cash Withdrawal above ₹1 crore",
    "Cash Withdrawal above ₹1 crore": "Cash Withdrawal above ₹1 crore",
    "Income from Banking": "Cash Withdrawal above ₹1 crore",
    "Cash Withdrawal from Bank": "Cash Withdrawal above ₹1 crore",
    "EPF Premature Withdrawal by Employee": "Premature EPF Withdrawal",

    # E-commerce
    "Income from business or profession": "E-commerce",
    "E-commerce Payment via Platform": "E-commerce",
    "E-commerce Payment to Vendor":"E-commerce",

    # Goods
    "Goods": "Purchase of Goods (Section 194Q)",
    "Goods (Section 194Q)": "Purchase of Goods (Section 194Q)",
    "Purchase of Raw Materials": "Purchase of Goods (Section 194Q)",
    "Raw Material Purchase": "Purchase of Goods (Section 194Q)",

    # Others
    "Courier Charges": "NIL",
    "Purchase of Computer Hardware": "NIL",
    "Purchase of Stationery": "NIL",
    "NIL": "NIL",
    "None (TDS not applicable)": "NIL",
    "None (below threshold or exempted)": "NIL",
    "Nil or Exempted": "NIL",

    # Commissions
    "Commission to Referral Partner": "Brokerage/Commission",
    "Commission on Lottery Sales": "Brokerage/Commission",
    "Brokerage Paid to Agent": "Brokerage/Commission",

    "Payment to Individual Contractor": "Contractor Payment",
    "Labour Contract": "Contractor Payment",

    "Payment to Freelancer for Design": "Freelance/Consultancy Work",
    "Freelance/Consultancy Work": "Freelance/Consultancy Work",
    "Payment to Foreign Sports Association": "Non-Resident Sports Association"


}




def clean_text(text: str) -> str:
    return text.strip().rstrip(',').lower()

def get_standard_category(predicted_category: str) -> str:
    cleaned = clean_text(predicted_category)
    for key, value in CATEGORY_MAP.items():
        if clean_text(key) == cleaned:
            return value
    return predicted_category.strip()

def get_rule_from_tds_rules(category: str):
    cleaned = clean_text(category)
    for key in TDS_RULES:
        if clean_text(key) == cleaned:
            return TDS_RULES[key]
    return None

def calculate_actual_tds_rate(item_text: str) -> str:
    try:
        parts = item_text.split(" - ")
        amount = float(parts[1].replace("₹", "").replace(",", "").strip())
        tds = float(parts[2].replace("TDS:", "").replace("₹", "").replace(",", "").strip())
        rate = round((tds / amount) * 100, 2)
        return f"{rate}%"
    except:
        return "Unknown"

def rates_match(predicted_rate: str, expected_rate: str) -> bool:
    return clean_text(predicted_rate) in clean_text(expected_rate)

def validate_tds(item_text: str, predicted_category: str, predicted_rate: str):
    standard_category = get_standard_category(predicted_category)
    rule = TDS_RULES.get(standard_category)

    result = {
        "item": item_text,
        "predicted_category": predicted_category,
        "predicted_rate": predicted_rate,
        "status": "",
        "expected_section": None,
        "expected_rate": None,
        "note": ""
    }

    if not rule:
        result["status"] = "Unknown Category"
        result["note"] = f"No TDS rule found for category '{standard_category}'"
        return result

    result["expected_section"] = rule["section"]
    result["expected_rate"] = rule["rate"]
    result["note"] = rule.get("note", "")

    if rates_match(predicted_rate, rule["rate"]):
        result["status"] = "Valid"
    else:
        result["status"] = "Mismatch"

    return result