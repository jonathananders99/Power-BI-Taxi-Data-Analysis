import os
import pandas as pd
from config import chunk_size, cur_path

def combine_csv_files(input_folder, output_file, chunk_size, taxi_type, header):
    # Delete the output file if it exists
    if os.path.exists(output_file):
        os.remove(output_file)

    # Print the header before processing any files
    pd.DataFrame(columns=header).to_csv(output_file, index=False)

    # Get the list of CSV files in the input folder
    csv_file_list = [file for file in os.listdir(input_folder) if file.endswith('.csv')]

    for csv_file_name in csv_file_list:
        file_path = os.path.join(input_folder, csv_file_name)

        chunk_container = pd.read_csv(file_path, chunksize=chunk_size, skiprows=1, header=None)
        rows_added = 0  # Variable to track the number of rows added

        for chunk in chunk_container:
            chunk["taxi_type"] = taxi_type  # Add taxi_type column and set values
            chunk.to_csv(output_file, mode="a", index=False, header=False)
            rows_added += len(chunk)

        print(f"Added {rows_added} rows from file: {csv_file_name}")

# Yellow
combine_csv_files(
    cur_path + "Data/Yellow Taxi/Individual CSVs", 
    cur_path + "Data/Yellow Taxi/all_yellow.csv", 
    chunk_size, 
    "Yellow Taxi", 
    ['VendorID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime', 'passenger_count', 'trip_distance', 
        'RatecodeID', 'store_and_fwd_flag', 'PULocationID', 'DOLocationID', 'payment_type', 'fare_amount', 
        'extra', 'mta_tax', 'tip_amount', 'tolls_amount', 'improvement_surcharge', 'total_amount', 
        'congestion_surcharge', 'airport_fee', 'taxi_type']
)

# Green
combine_csv_files(
    cur_path + "Data/Green Taxi/Individual CSVs", 
    cur_path + "Data/Green Taxi/all_green.csv", 
    chunk_size, 
    "Green Taxi", 
    ['VendorID', 'lpep_pickup_datetime', 'lpep_dropoff_datetime', 'store_and_fwd_flag', 'RatecodeID',
        'PULocationID', 'DOLocationID', 'passenger_count', 'trip_distance', 'fare_amount', 'extra', 'mta_tax',
        'tip_amount', 'tolls_amount', 'ehail_fee', 'improvement_surcharge', 'total_amount', 'payment_type',
        'trip_type', 'congestion_surcharge', 'taxi_type']
)
