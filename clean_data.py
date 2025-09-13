import pandas as pd

# Path to Excel file
file_path = r"C:\Users\gold\Documents\python\porject-2\ICRISAT-District Level Data.xlsx"

# Read Excel
df = pd.read_excel(file_path)

# 1) Clean column names (lowercase, underscores, remove brackets)
df.columns = (
    df.columns.str.strip()       # remove spaces at ends
              .str.lower()       # convert to lowercase
              .str.replace(" ", "_")   # spaces -> underscores
              .str.replace("(", "")    # remove (
              .str.replace(")", "")    # remove )
)

# 2) Replace obvious missing values if any (just in case)
df = df.replace({999999: pd.NA, -9999: pd.NA})

# 3) Save cleaned file as CSV for easier use later
out_path = r"C:\Users\gold\Documents\python\porject-2\icrisat_clean.csv"
df.to_csv(out_path, index=False)

print("✅ Cleaned data saved to:", out_path)
print("Shape:", df.shape)
print("First 5 rows:")
print(df.head())
