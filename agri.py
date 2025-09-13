import pandas as pd

# Path to your Excel file
file_path = r"C:\Users\gold\Documents\python\porject-2\ICRISAT-District Level Data.xlsx"

# Read Excel file
df = pd.read_excel(file_path)

# Show first 5 rows
print("First 5 rows:")
print(df.head())

# Show shape (rows, columns)
print("\nShape of dataset:", df.shape)

# Show all column names
print("\nColumns:", df.columns.tolist())


