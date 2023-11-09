import os
import pandas as pd

# Set the path to the folder containing the CSV files
folder_path = 'D:\JDE7\mid\0810csv' #<---- your folder wanna merge!!!!

# Initialize an empty DataFrame to store the combined data
combined_data = pd.DataFrame()

# Define the chunk size for reading and merging
chunk_size = 10000

# Iterate over each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)

        # Read the CSV file
        df = pd.read_csv(file_path)

        # Extract the 'Name' and ' Price' columns
        df = df[['product_name', 'price']]

        # Rename the 'Price' column to include the file name
        df = df.rename(columns={'price': f'price({filename})'})

        # Merge the data based on the 'Name' column
        if combined_data.empty:
            combined_data = df
        else:
            combined_data = combined_data.merge(df, on='product_name', how='inner')

# Calculate the price difference for each pair of columns
price_columns = combined_data.filter(regex='price').columns
combined_data['Price Difference'] = combined_data[price_columns].max(axis=1) - combined_data[price_columns].min(axis=1)

# Display the merged data with the price difference
print(combined_data)