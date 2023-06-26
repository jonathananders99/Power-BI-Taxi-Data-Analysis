import os
import pandas as pd
from config import chunk_size, cur_path


# New header for the csv file
new_header = ['taxi_type', 'pickup_date', 'day_type', 'pickup_time', 'hourly_times', 'total_time', 'grouped_total_times', 'passenger_count', 'passenger_count_grouped', 'trip_distance', 'payment_type', 'tip_amount', 'fare_charge', 'total_charged']






# ****************YELLOW TAXI****************
source_file = cur_path + 'Data/Yellow Taxi/all_yellow.csv'
target_file = cur_path + 'Data/all_data.csv'

# Specify the columns to remove
columns_to_remove = ['VendorID', 'store_and_fwd_flag', 'PULocationID', 'DOLocationID', 'fare_amount', 'extra', 'mta_tax', 'tolls_amount', 'improvement_surcharge', 'congestion_surcharge', 'airport_fee', 'tpep_dropoff_datetime', 'RatecodeID']

# Specify the column name changes
column_name_changes = {
    'tpep_pickup_datetime': 'pickup_date',
    'total_amount': 'fare_charge',
}

# Delete the target file if it already exists
if os.path.exists(target_file):
    os.remove(target_file)

# Write the cleaned headers to the target file
with open(target_file, 'w') as f:
    f.write(','.join(new_header) + '\n')

# Function to clean a chunk of data and append it to the target file
def clean_chunk_and_append_yellow(chunk):

    # Rename columns
    chunk = chunk.rename(columns=column_name_changes)

    # Convert date columns to datetime
    chunk['pickup_date'] = pd.to_datetime(chunk['pickup_date'])
    chunk['tpep_dropoff_datetime'] = pd.to_datetime(chunk['tpep_dropoff_datetime'])

    # Filter rows within the desired years (2018-2022)
    chunk = chunk[(chunk['pickup_date'].dt.year >= 2018) & (chunk['pickup_date'].dt.year <= 2022)]

    # Calculate time difference in minutes and round to 2 decimal places
    chunk['total_time'] = round((chunk['tpep_dropoff_datetime'] - chunk['pickup_date']).dt.total_seconds() / 60, 2)

    # Extract time from pickup_date in HH:MM format
    chunk['pickup_time'] = chunk['pickup_date'].dt.strftime("%H:%M")

    # Extract date from pickup_date
    chunk['pickup_date'] = chunk['pickup_date'].dt.date

    # Remove parentheses from certain columns
    columns_to_remove_parentheses = ['tip_amount', 'fare_charge']
    chunk[columns_to_remove_parentheses] = chunk[columns_to_remove_parentheses].replace({'(': '', ')': ''}, regex=True)

    # Add new column
    chunk['total_charged'] = chunk['tip_amount'] + chunk['fare_charge']

    # Replace missing values in passenger_count with 1
    chunk['passenger_count'] = chunk['passenger_count'].fillna(1)

    # Replace missing values in payment_type with 1
    chunk['payment_type'] = chunk['payment_type'].fillna(1)

    # Remove unwanted columns
    chunk = chunk.drop(columns=columns_to_remove)

    # Apply additional filtering conditions
    chunk = chunk[
        (chunk['total_time'] >= 0) & (chunk['total_time'] <= 2000) &
        (chunk['passenger_count'] < 32) &
        (chunk['trip_distance'] >= 0) & (chunk['trip_distance'] <= 1000) &
        (chunk['tip_amount'] >= 0) & (chunk['tip_amount'] <= 2000) &
        (chunk['fare_charge'] >= 0) & (chunk['fare_charge'] <= 5000) &
        (chunk['total_charged'] >= 0) & (chunk['total_charged'] <= 3000)
    ]
    
    # Change payment_type column to its values
    payment_types = {
        1: 'Credit Card',
        2: 'Cash',
        3: 'No Charge',
        4: 'Dispute',
        5: 'Unknown'
    }
    chunk['payment_type'] = chunk['payment_type'].map(payment_types)

    # Create hourly_times column
    chunk['hourly_times'] = chunk['pickup_time'].str[:2].apply(lambda x: x.zfill(2))

    # Create passenger_count_grouped column
    chunk.loc[chunk['passenger_count'] >= 7, 'passenger_count_grouped'] = '7+'
    chunk.loc[chunk['passenger_count'] < 7, 'passenger_count_grouped'] = chunk.loc[chunk['passenger_count'] < 7, 'passenger_count'].astype(int)


    # Create grouped_total_times column
    time_groups = {
        (0, 9.999): '0-10',
        (10, 19.999): '10-20',
        (20, 29.999): '20-30',
        (30, 39.999): '30-40',
        (40, 49.999): '40-50',
        (50, 59.999): '50-60'
    }
    chunk['grouped_total_times'] = pd.cut(chunk['total_time'], bins=[0, 10, 20, 30, 40, 50, 60, float('inf')], labels=[val for val in time_groups.values()] + ['60+'], right=False)

    # Create day_type column
    chunk['day_type'] = pd.to_datetime(chunk['pickup_date']).dt.dayofweek // 5 == 0
    chunk['day_type'] = chunk['day_type'].map({True: 'Weekday', False: 'Weekend'})

    # Reorder columns
    chunk = chunk[new_header]

    # Append cleaned chunk to the target file
    chunk.to_csv(target_file, mode='a', header=False, index=False)


# Read the source file in chunks and clean each chunk
for chunk in pd.read_csv(source_file, chunksize=chunk_size):
    clean_chunk_and_append_yellow(chunk)




# ****************Green TAXI****************
source_file = cur_path + 'Data/Green Taxi/all_green.csv'
target_file = cur_path + 'Data/all_data.csv'

# Specify the columns to remove
columns_to_remove = ['VendorID', 'lpep_dropoff_datetime', 'store_and_fwd_flag', 'RatecodeID', 'PULocationID', 'DOLocationID', 'fare_amount', 'extra', 'mta_tax', 'tolls_amount', 'ehail_fee', 'improvement_surcharge', 'trip_type', 'congestion_surcharge']


# Specify the column name changes
column_name_changes = {
    'lpep_pickup_datetime': 'pickup_date',
    'total_amount': 'fare_charge',
}


# Function to clean a chunk of data and append it to the target file
def clean_chunk_and_append_green(chunk):

    # Rename columns
    chunk = chunk.rename(columns=column_name_changes)

    # Convert date columns to datetime
    chunk['pickup_date'] = pd.to_datetime(chunk['pickup_date'])
    chunk['lpep_dropoff_datetime'] = pd.to_datetime(chunk['lpep_dropoff_datetime'])

    # Filter rows within the desired years (2018-2022)
    chunk = chunk[(chunk['pickup_date'].dt.year >= 2018) & (chunk['pickup_date'].dt.year <= 2022)]

    # Calculate time difference in minutes and round to 2 decimal places
    chunk['total_time'] = round((chunk['lpep_dropoff_datetime'] - chunk['pickup_date']).dt.total_seconds() / 60, 2)

    # Extract time from pickup_date in HH:MM format
    chunk['pickup_time'] = chunk['pickup_date'].dt.strftime("%H:%M")

    # Extract date from pickup_date
    chunk['pickup_date'] = chunk['pickup_date'].dt.date

    # Add new column
    chunk['total_charged'] = chunk['tip_amount'] + chunk['fare_charge']
    
    # Replace missing values in passenger_count with 1
    chunk['passenger_count'] = chunk['passenger_count'].fillna(1)
    
    # Replace missing values in payment_type with 1
    chunk['payment_type'] = chunk['payment_type'].fillna(1)

    # Remove unwanted columns
    chunk = chunk.drop(columns=columns_to_remove)
    
    # Apply additional filtering conditions
    chunk = chunk[
        (chunk['total_time'] >= 0) & (chunk['total_time'] <= 2000) &
        (chunk['passenger_count'] < 32) &
        (chunk['trip_distance'] >= 0) & (chunk['trip_distance'] <= 1000) &
        (chunk['tip_amount'] >= 0) & (chunk['tip_amount'] <= 2000) &
        (chunk['fare_charge'] >= 0) & (chunk['fare_charge'] <= 5000) &
        (chunk['total_charged'] >= 0) & (chunk['total_charged'] <= 3000)
    ]
    
    # Change payment_type column to its values
    payment_types = {
        1: 'Credit Card',
        2: 'Cash',
        3: 'No Charge',
        4: 'Dispute',
        5: 'Unknown'
    }
    chunk['payment_type'] = chunk['payment_type'].map(payment_types)

    # Create hourly_times column
    chunk['hourly_times'] = chunk['pickup_time'].str[:2].apply(lambda x: x.zfill(2))

    # Create passenger_count_grouped column
    chunk.loc[chunk['passenger_count'] >= 7, 'passenger_count_grouped'] = '7+'
    chunk.loc[chunk['passenger_count'] < 7, 'passenger_count_grouped'] = chunk.loc[chunk['passenger_count'] < 7, 'passenger_count'].astype(int)

    # Create grouped_total_times column
    time_groups = {
        (0, 9.999): '0-10',
        (10, 19.999): '10-20',
        (20, 29.999): '20-30',
        (30, 39.999): '30-40',
        (40, 49.999): '40-50',
        (50, 59.999): '50-60'
    }
    chunk['grouped_total_times'] = pd.cut(chunk['total_time'], bins=[0, 10, 20, 30, 40, 50, 60, float('inf')], labels=[val for val in time_groups.values()] + ['60+'], right=False)

    # Create day_type column
    chunk['day_type'] = pd.to_datetime(chunk['pickup_date']).dt.dayofweek // 5 == 0
    chunk['day_type'] = chunk['day_type'].map({True: 'Weekday', False: 'Weekend'})
    
    # Reorder columns
    chunk = chunk[new_header]  # Include other columns as necessary

    # Append the cleaned chunk to the target file
    chunk.to_csv(target_file, mode='a', header=False, index=False)


# Process each chunk of data and append it to the target file
for chunk in pd.read_csv(source_file, chunksize=chunk_size):
    clean_chunk_and_append_green(chunk)