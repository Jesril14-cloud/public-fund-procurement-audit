Public Fund and Procurement Audit Pipeline
Forensic data analysis and SQL audit pipeline tracking public fund disbursements and contract awards to detect procurement red flags.

Overview
This project analyzes public procurement contract awards to identify supplier monopolies, high-frequency repeat awards, and high-value capital allocation outliers using SQL and Python.

Objectives
1. Identify high-risk vendor concentration where select contractors capture disproportionate shares of public funding.
2. Detect potential procurement splitting or recurring contract awards.
3. Isolate multi-million dollar capital outlay contracts exceeding threshold audit benchmarks.

Tech Stack
* SQL (DuckDB): Data extraction, aggregation, numerical type casting, string cleaning
* Python: Automated data pipeline and export execution
* Dataset: World Bank Corporate Procurement Contract Awards

Audit Findings Summary
* Top supplier allocations and repeat vendor win frequencies were identified and ranked by cumulative contract value.
* Contracts exceeding 10 million dollars were isolated and exported for manual compliance audit in flagged_high_value_contracts.csv.

How to Run
1. Install dependencies:
   pip install duckdb pandas
2. Run the audit pipeline:
   python scripts/audit_procurement.py