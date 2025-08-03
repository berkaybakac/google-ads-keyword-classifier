# Google Ads Keyword Classifier (GPT-4o Playground Project)

This repository contains a structured prompt-driven classification system designed to help third-party repair businesses classify Google Ads search terms using OpenAI GPT-4o-mini in Playground.

The goal is to minimize budget waste by accepting **only** highly relevant search queries that show clear intent for third-party repair/service in a specified city and sector (e.g., "çamaşır makinesi servisi in Istanbul").

---

## How It Works

The system uses a dynamic prompt template with the following placeholders:

- `{{CITY}}` — The target service location (e.g., `ISTANBUL`)
- `{{SECTOR}}` — The repair/service domain (e.g., `BEYAZ EŞYA`, `KLİMA`, `KOMBİ`)

Search terms are passed into the Playground in batches (e.g., 50–100 terms), and the model returns structured JSON with the following schema:

```json
{
  "results": [
    {
      "id": 1,
      "term": "kadıköy çamaşır makinesi tamircisi",
      "is_positive": 1,
      "match_type": "exact",
      "explanation": "Accepted. Query shows clear third-party repair intent for ÇAMAŞIR MAKİNESİ in ISTANBUL."
    },
    ...
  ]
}
```

---

## Project Structure

```
GOOGLE-ADS-KEYWORD-CLASSIFIER/
│
├── prompts/                          # Prompt templates and model outputs
│   ├── 01_response_schema.json       # JSON schema for classification results
│   ├── 02_system_prompt_Dinamic_Main.txt   # Dynamic system prompt (main version)
│   ├── 03_user_prompt_New_Example.txt      # Sample user prompt for Playground
│   ├── 04_output_*                   # JSON result files for different city/sector combinations
│
├── prompts_tests/                   # (Optional) Test input or validation assets
├── json_to_excel_converter.py       # Python script to convert output JSON to Excel
├── keyword_report.xlsx              # Output Excel report (converted from JSON)
├── Search_Terms.txt                 # Input search terms for testing
├── README.md                        # 📄 You are here
└── .gitignore
```

---

## Prompt Logic Highlights

- **City Filter:** Only terms within `{{CITY}}` are accepted. Known districts inside the city (e.g., Kadıköy ∈ Istanbul) are valid.
- **Service Intent:** Queries must include keywords like `tamir`, `tamircisi`, `onarım`, `servis`, `arıza`, `çalışmıyor`.
- **Brand-Only Filter:** Queries like `"Arçelik buzdolabı"` are rejected unless service intent is also present.
- **Official Service Filter:** Phrases like `yetkili servis`, `müşteri hizmetleri`, or brand support lines are rejected.

---

## Model Testing

Extensive testing has been performed across multiple city-sector pairs:

- Istanbul - Televizyon Servisi (0 errors in 50)
- Ankara - Klima Servisi (1 explanation mismatch in 50)
- Istanbul - Beyaz Eşya (1 match_type mismatch in 64)
- Ankara - Kombi (1 incorrect positive in 50)
- Istanbul - Çamaşır Makinesi (1 explanation error, 2 subjective borderline rejections in 50)

> **Note:** When using sample outputs, ensure example cities/districts match the chosen `{{CITY}}`. For example, if `{{CITY}} = Ankara`, then Eryaman should be considered valid; otherwise, reject it.

---

## Final Prompt Template

The full dynamic prompt is located in:

```
prompts/02_system_prompt_Dinamic_Main.txt
```

You must replace `{{CITY}}` and `{{SECTOR}}` with your target parameters before pasting into Playground.

---

## Converting JSON to Excel

To convert a `.json` classification output to `.xlsx`:

```bash
python json_to_excel_converter.py
```

Output: `keyword_report.xlsx`

---

## Notes

- Built for use with **GPT-4o-mini** on **OpenAI Playground**
- Optimized for large-scale batch classification (up to 8,000+ terms)
- Every `04_output_*.json` file contains tested and verified samples

---

## License

MIT License – free to use, modify, and distribute.

---

## Contact

Maintained by [Berkay Bakaç](https://github.com/berkaybakac)  
For feedback or contributions, feel free to open an issue or pull request.