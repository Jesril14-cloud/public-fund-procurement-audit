import duckdb
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to database and load data
con = duckdb.connect(database=':memory:')
con.execute("""
    CREATE TABLE contracts AS 
    SELECT * FROM read_csv_auto('procurement_contracts.csv', ignore_errors=true);
""")

# Query top 10 suppliers by total value
query = """
    SELECT 
        "Supplier" AS supplier,
        ROUND(SUM(TRY_CAST(REPLACE(REPLACE(CAST("Contract Award Amount" AS VARCHAR), '$', ''), ',', '') AS DOUBLE)) / 1000000, 2) AS total_millions
    FROM contracts
    WHERE "Supplier" IS NOT NULL
    GROUP BY "Supplier"
    ORDER BY total_millions DESC
    LIMIT 10;
"""

df_top = con.execute(query).df()

# Configure chart style
plt.figure(figsize=(10, 6))
sns.barplot(data=df_top, x='total_millions', y='supplier', palette='rocket')

plt.title('Top 10 Suppliers by Total Award Value (in Millions USD)', fontsize=14, weight='bold')
plt.xlabel('Total Contract Value ($M USD)', fontsize=12)
plt.ylabel('Supplier Name', fontsize=12)
plt.tight_layout()

# Save the visualization image
plt.savefig('top_suppliers_risk.png', dpi=300)
print("[SUCCESS] Chart saved as 'top_suppliers_risk.png'")

# Display the interactive window
plt.show()