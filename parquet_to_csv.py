import os
import pandas as pd
import pyarrow.parquet as pq
from config import chunk_size, cur_path


def convert_parquet_to_csv(input_folder, output_folder):
    # List of all files in the input directory
    files = os.listdir(input_folder)
    
    # Filter the list down to only .parquet files
    parquet_files = [f for f in files if f.endswith('.parquet')]

    # Process each parquet file
    for file in parquet_files:
        # Construct the full path to the file
        parquet_file_path = os.path.join(input_folder, file)

        # Read the parquet file
        df = pd.read_parquet(parquet_file_path)

        # Construct the path to the output csv file
        csv_file_path = os.path.join(output_folder, f"{os.path.splitext(file)[0]}.csv")

        # Write the DataFrame to a csv file
        df.to_csv(csv_file_path, index=False)

        print(f"Converted {parquet_file_path} to {csv_file_path}")

# Green
convert_parquet_to_csv(cur_path + 'Data/Green Taxi/Parquet Files', cur_path + 'Data/Green Taxi/Individual CSVs')

# Yellow
convert_parquet_to_csv(cur_path + 'Data/Yellow Taxi/Parquet Files', cur_path + 'Data/Yellow Taxi/Individual CSVs')
