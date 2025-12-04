import pandas as pd

# List your CSV file names
csv_files = ['magnit-data.csv', 'rigla-data.csv', 'aptekaru-data.csv']

# Create an empty DataFrame to store the combined data
# df_combined = pd.DataFrame()
df = pd.concat(map(pd.read_csv, csv_files), ignore_index=True)

# Loop through the files and append each one to the combined DataFrame
# for file in csv_files:
#     df = pd.read_csv(file)
#     df_combined = df_combined.append(df, ignore_index=True)

# Optional: Save the combined DataFrame
df.to_csv("data.csv", index=False)

print(df.head())
