
# tds_categorizer_llm.py
import os
import re
import json
import together
import ast
from dotenv import load_dotenv

from agents.tds_validator import CATEGORY_MAP

load_dotenv()
client = together.Together(api_key=os.getenv("TOGETHER_API_KEY"))

def extract_tds_rate(item_str):
    try:
        match = re.search(r'[-–—]\s*(\d[\d,]*)\s*[-–—]\s*TDS:\s*(\d+)', item_str)
        if not match:
            print(f"[DEBUG] No match found for: {item_str}")
            return "0%"
        amount_str, tds_str = match.groups()
        amount = float(amount_str.replace(",", "").strip())
        tds = float(tds_str.strip())
        rate = round((tds / amount) * 100, 2)
        return f"{int(rate)}%" if rate.is_integer() else f"{rate}%"
    except Exception as e:
        print(f"[ERROR in extract_tds_rate]: {e}")
        return "0%"


def extract_json_string(text: str) -> str:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r'\{[\s\S]*?\}', text)
        if match:
            try:
                return json.loads(match.group(0))
            except:
                return ast.literal_eval(match.group(0))
        raise ValueError("No valid JSON object found in LLM response.")

def get_tds_from_llm(line_item: str):
    prompt = f"""
    You are a TDS expert. For the given Indian invoice line item, return the appropriate TDS category and TDS rate.

    Choose ONLY from the below categories (return exactly as-is):
    - "Professional or Technical Services"
    - "Brokerage/Commission"
    - "Property Sale"
    - "Rent"
    - "Life Insurance Maturity"
    - "Interest from Bank/Post Office"
    - "Purchase of Goods (Section 194Q)"
    - "Dividend"
    - "Premature EPF Withdrawal"
    - "Cash Withdrawal above ₹1 crore"
    - "E-commerce"
    - "NIL"

    Format:
    {{
      "category": "<choose one>",
      "tds_rate": "<e.g. 10% >"
    }}
    Important Rules:
- ONLY return the JSON object.
- DO NOT add any explanation or text outside the JSON.


    If you're unsure or if no TDS applies, return:
    {{ "category": "NIL", "tds_rate": "0%" }}

    Line item: "{line_item}"
    """

    try:
        response = client.chat.completions.create(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        result = response.choices[0].message.content.strip()
        print("LLM Response:\n", result)

        result_dict = extract_json_string(result)

        calculated_rate = extract_tds_rate(line_item)
        if result_dict.get("category") == "NIL" and calculated_rate != "0%":
            line_lower = line_item.lower()
            matched = False
            for keyword, category in CATEGORY_MAP.items():
                if keyword.lower() in line_lower:
                    result_dict["category"] = category
                    matched = True
                    break
            if not matched:
                result_dict["category"] = "Uncategorized"
            result_dict["tds_rate"] = calculated_rate

        # Apply override from CATEGORY_MAP
        for keyword, mapped_category in CATEGORY_MAP.items():
            if keyword.lower() in line_item.lower():
                result_dict["category"] = mapped_category
                break

        # Now return final result
        return {
            "item": line_item.strip(),
            "category": result_dict.get("category", "Unknown"),
            "tds_rate": extract_tds_rate(line_item)
        }


    except Exception as e:
        return {
            "item": line_item.strip(),
            "category": "ParseError",
            "tds_rate": "N/A",
            "error": str(e)
        }

def auto_categorize_tds_llm(text: str):
    lines = text.strip().splitlines()
    item_lines = [line for line in lines if line.strip().lower().startswith("item:")]
    cleaned_items = [line.replace("Item:", "").strip() for line in item_lines]
    results = [get_tds_from_llm(item) for item in cleaned_items]
    return {"tds_categorization": results}

