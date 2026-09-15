import duckdb

csv_file = "procurement_contracts.csv"
con = duckdb.connect(database=':memory:')

# Read CSV directly into an in-memory SQL table
con.execute(f"""
    CREATE TABLE contracts AS 
    SELECT * FROM read_csv_auto('{csv_file}', ignore_errors=true);
""")

print("--- Data Schema Loaded Successfully ---")

# Print all available columns so we know the exact field names
cols = con.execute("DESCRIBE contracts").df()
print("\nActual Columns in Dataset:")
print(cols[['column_name', 'column_type']].to_string(index=False))

# ==============================================================================
# AUDIT TEST 1: VENDOR CONCENTRATION RISK
# Identifies vendors taking the largest share of public contract funds
# ==============================================================================
print("\n--- TOP 10 CONTRACTORS BY TOTAL AWARD VALUE ---")
query_vendor_risk = """
    SELECT 
        "Supplier" AS supplier_name,
        COUNT(*) AS total_contracts_won,
        ROUND(SUM(TRY_CAST(REPLACE(REPLACE(CAST("Contract Award Amount" AS VARCHAR), '$', ''), ',', '') AS DOUBLE)), 2) AS total_amount_awarded
    FROM contracts
    WHERE "Supplier" IS NOT NULL
    GROUP BY "Supplier"
    ORDER BY total_amount_awarded DESC
    LIMIT 10;
"""
print(con.execute(query_vendor_risk).df())

# ==============================================================================
# AUDIT TEST 2: SINGLE-SUPPLIER WIN FREQUENCY
# Flags vendors receiving repeated awards
# ==============================================================================
print("\n--- TOP FREQUENT SUPPLIERS (BY CONTRACT COUNT) ---")
query_frequent_wins = """
    SELECT 
        "Supplier" AS supplier,
        COUNT(*) AS contracts_count,
        ROUND(AVG(TRY_CAST(REPLACE(REPLACE(CAST("Contract Award Amount" AS VARCHAR), '$', ''), ',', '') AS DOUBLE)), 2) AS avg_contract_value
    FROM contracts
    WHERE "Supplier" IS NOT NULL
    GROUP BY "Supplier"
    HAVING COUNT(*) > 5
    ORDER BY contracts_count DESC
    LIMIT 10;
"""
print(con.execute(query_frequent_wins).df())

# ==============================================================================
# AUDIT TEST 3: EXPORT HIGH-VALUE AWARDS
# Filters and exports multi-million dollar contracts for closer audit review
# ==============================================================================
export_query = """
    COPY (
        SELECT 
            "Supplier" AS supplier,
            "Contract Description" AS description,
            TRY_CAST(REPLACE(REPLACE(CAST("Contract Award Amount" AS VARCHAR), '$', ''), ',', '') AS DOUBLE) AS award_amount
        FROM contracts
        WHERE TRY_CAST(REPLACE(REPLACE(CAST("Contract Award Amount" AS VARCHAR), '$', ''), ',', '') AS DOUBLE) > 10000000
        ORDER BY award_amount DESC
    ) TO 'flagged_high_value_contracts.csv' (HEADER, DELIMITER ',');
"""
con.execute(export_query)
print("\n[SUCCESS] Exported high-value awards to 'flagged_high_value_contracts.csv'")