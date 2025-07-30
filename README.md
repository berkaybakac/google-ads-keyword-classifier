# Prompt-Based Keyword Classifier for Local Google Ads Targeting

This project showcases how OpenAI Playground can be used to build a lightweight, prompt-powered classification system for Google Ads search terms — specifically for a white goods repair company operating in Istanbul.

---

## Project Focus

Unlike conventional data processing projects, the core of this work lies in **prompt engineering and LLM utilization**. Most of the effort went into:

- Crafting an effective `system` prompt that simulates a domain expert,
- Writing a structured `user` prompt that clearly defines task goals and constraints,
- Designing a robust `JSON schema` to guide GPT’s output,
- Iteratively testing prompts in OpenAI Playground for consistent and high-quality results.

The **primary product** of this project is a structured, AI-generated dataset containing classification decisions for 30 real-world search terms.

---

## Use Case

For each keyword, the model answers:
- Should this term trigger an ad? (`is_positive`)
- What kind of match type should be applied? (`match_type`)
- Why? (`explanation`)

The output enables **automated ad targeting decisions** without manual rule-writing or human labeling.

---

## File Structure

```
.
├── json_to_excel_converter.py       # Python script to export JSON results to Excel
├── gelismis_output.xlsx             # Final structured output (optional)
├── prompts/
│   ├── 01_system_prompt.txt         # Defines GPT's role and tone
│   ├── 02_user_prompt.txt           # Task definition and input format
│   ├── 03_response_schema.txt       # Output format contract (JSON)
│   └── 04_ai_output_sample.json     # Playground output with 30 labeled terms
├── .vscode/
│   └── settings.json                # Project-level interpreter configuration
├── .gitignore
└── README.md
```

---

## Running the Script (optional)

Once the AI-generated results are saved as `04_ai_output_sample.json`, they can be exported to a styled Excel sheet for business use.

```bash
pip install pandas openpyxl
python json_to_excel_converter.py
```

This step is included to enable **non-technical stakeholders** to review or filter the results easily.

---

## Sample Output Row

| term                          | is_positive | match_type | explanation                                                  |
|------------------------------|-------------|------------|--------------------------------------------------------------|
| alibeyköy buzdolabı tamircisi | 1           | exact      | High-intent, local repair-focused query for fridge repair.   |

---

## Why This Matters

This project highlights how:
- A single well-engineered prompt + schema can automate complex classification tasks,
- OpenAI Playground can act as a low-code labeling assistant,
- Prompt engineering can become a **practical decision-making tool** for digital marketing.

---

## Future Extensions

- Bulk term input & auto-processing via OpenAI API
- CSV export for Google Ads Editor compatibility
- UI for business teams to review & override AI decisions

---

## Author Note

The majority of time in this project was spent designing, testing, and refining the prompts in OpenAI Playground — not on coding or automation.  
The technical code (JSON → Excel) supports the prompt-based insight and decision structure.

This project serves as a minimal but powerful showcase of what LLMs can do when paired with clear instruction and schema design.

---
