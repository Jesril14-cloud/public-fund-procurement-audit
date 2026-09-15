import pandas as pd

# Load only the first 5 rows to read the schema instantly
df = pd.read_csv("procurement_contracts.csv", nrows=5)

print("Total columns found:", len(df.columns))
print("\nList of all columns:")
for i, col in enumerate(df.columns):
    print(f"{i}: {col}")