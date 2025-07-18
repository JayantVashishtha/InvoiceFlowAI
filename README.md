# 🧾 Demo_PayableGPT — LLM + Rule-based TDS Categorization System

This project is an AI-powered invoice processing pipeline that:
- Extracts data from invoices
- Predicts the appropriate TDS category using an LLM (via Together API)
- Validates predicted results using Indian Income Tax rules
- Flags mismatches and duplicate invoices
- Sends automated vendor replies

Built with ❤️ using Python, Together AI, and rule-based matching.


---

## 🚀 Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/Demo_PayableGPT.git
cd Demo_PayableGPT_Dice
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Key
```bash
Create a .env file in the root directory:
TOGETHER_API_KEY=your_together_api_key
```


