-- Query 1: Vendor Concentration by Total Award Value
SELECT 
    "Supplier" AS supplier_name,
    COUNT(*) AS total_contracts_won,
    ROUND(SUM(TRY_CAST(REPLACE(REPLACE(CAST("Contract Award Amount" AS VARCHAR), '$', ''), ',', '') AS DOUBLE)), 2) AS total_amount_awarded
FROM contracts
WHERE "Supplier" IS NOT NULL
GROUP BY "Supplier"
ORDER BY total_amount_awarded DESC
LIMIT 10;

-- Query 2: Repeated Vendor Wins (Monopoly / Collusion Risk)
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

-- Query 3: Multi-Million Outlier Contracts (> $10M)
SELECT 
    "Supplier" AS supplier,
    "Contract Description" AS description,
    TRY_CAST(REPLACE(REPLACE(CAST("Contract Award Amount" AS VARCHAR), '$', ''), ',', '') AS DOUBLE) AS award_amount
FROM contracts
WHERE TRY_CAST(REPLACE(REPLACE(CAST("Contract Award Amount" AS VARCHAR), '$', ''), ',', '') AS DOUBLE) > 10000000
ORDER BY award_amount DESC;