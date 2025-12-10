import time
import random
import requests
import pandas as pd
import os
import sys

# --- Configuration ---
URL = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSfeLPNWwoaPjqLIImZ-te6dP8b4zOlslGrJsd4bicmw49klkQ/formResponse"
CSV_FILENAME = "sleep_data_1000.csv"
NUM_RECORDS = 1000
# Set to 30 seconds for a good balance between safety and avoiding GitHub's 6-hour job timeout.
SUBMISSION_DELAY_SECONDS = 30 

# --- Entry ID Mapping (Confirmed Working Structure) ---
# Maps the column names used in the CSV to the Google Form Entry IDs
ID_MAP = {
    "age": "entry.130782805", 
    "sleep_time": "entry.206918368", 
    "avg_sleep_hours": "entry.1315476675", 
    "wake_ups": "entry.882704943", 
    "smartphone_hours": "entry.1934504077", 
    "use_before_sleep": "entry.744326918",
    "stress_level": "entry.1784191715", 
    "caffeine_freq": "entry.1192970950",
    "screen_time_post_8pm": "entry.927479717",
    "exercise_days": "entry.2035929357",
    "difficulty_asleep": "entry.38757470",
    "time_to_sleep": "entry.1406815052",
    "weekend_sleep": "entry.1403062670",
    "fresh_after_waking": "entry.881978082",
    "sleep_quality": "entry.1026336142",
    "satisfaction": "entry.491147406"
}

def generate_csv(num_records):
    """Generates a CSV file with randomized, realistic data if it doesn't already exist."""
    # This check prevents regeneration of 1000 rows on every GitHub Action run
    if os.path.exists(CSV_FILENAME):
        print(f"✅ CSV file '{CSV_FILENAME}' already exists. Skipping generation.")
        return
        
    print(f"Generating {num_records} random records...")
    
    data = {}
    
    # Generate data for each field based on realistic weights
    data['age'] = [random.randint(18, 35) for _ in range(num_records)]
    data['sleep_time'] = random.choices(["Before 10 PM", "10 PM - 12 AM", "12 AM - 2AM", "After 2 AM"], weights=[15, 45, 30, 10], k=num_records)
    data['avg_sleep_hours'] = random.choices([4, 5, 6, 7, 8, 9], weights=[5, 10, 20, 30, 25, 10], k=num_records)
    data['wake_ups'] = random.choices([0, 1, 2, 3], weights=[30, 40, 20, 10], k=num_records)
    data['smartphone_hours'] = random.choices([3, 4, 5, 6, 7, 8], weights=[10, 20, 30, 20, 10, 10], k=num_records)
    data['use_before_sleep'] = random.choices(["Yes", "No"], weights=[75, 25], k=num_records)
    data['stress_level'] = random.choices([1, 2, 3, 4, 5], weights=[5, 15, 35, 30, 15], k=num_records)
    data['caffeine_freq'] = random.choices(["Never", "Rarely", "Often", "Daily"], weights=[10, 20, 30, 40], k=num_records)
    data['screen_time_post_8pm'] = random.choices(["Less than 1 hour", "1-2 hours", "2-4 hours", "More than 4 hours"], weights=[10, 30, 40, 20], k=num_records)
    data['exercise_days'] = random.choices(["0 days", "1-2 days", "3-4 days", "5+ days"], weights=[15, 30, 35, 20], k=num_records)
    data['difficulty_asleep'] = random.choices(["Never", "Rarely", "Sometimes", "Frequently", "Always"], weights=[25, 35, 25, 10, 5], k=num_records)
    data['time_to_sleep'] = random.choices(["Less than 10 minutes", "10-20 minutes", "20-40 minutes", "More than 40 minutes"], weights=[30, 40, 20, 10], k=num_records)
    data['weekend_sleep'] = random.choices(["Yes, Sleep more", "Yes, Sleep less", "No, Same schedule"], weights=[50, 10, 40], k=num_records)
    data['fresh_after_waking'] = random.choices(["Yes", "Sometimes", "No"], weights=[20, 60, 20], k=num_records)
    data['sleep_quality'] = random.choices([1, 2, 3, 4, 5], weights=[5, 10, 30, 35, 20], k=num_records)
    data['satisfaction'] = random.choices([1, 2, 3, 4, 5], weights=[5, 10, 25, 35, 25], k=num_records)

    # Create DataFrame and save to CSV
    df = pd.DataFrame(data)
    df.to_csv(CSV_FILENAME, index=False)
    print(f"✅ CSV file '{CSV_FILENAME}' created successfully with {num_records} records.")


def submit_from_csv(start_index):
    """Reads the CSV file and submits data row by row, starting from start_index."""
    
    if not os.path.exists(CSV_FILENAME):
        print(f"❌ Error: CSV file '{CSV_FILENAME}' not found. Run generate_csv() first.")
        return

    df = pd.read_csv(CSV_FILENAME)
    total_records = len(df)
    
    if start_index >= total_records:
        print(f"🎉 Submission complete! Start index ({start_index}) exceeds total records ({total_records}).")
        return

    print(f"\n--- Starting submission from record #{start_index + 1} of {total_records} ---")
    
    for index in range(start_index, total_records):
        row = df.iloc[index]
        
        # 1. Create the payload dictionary using the ID_MAP
        payload = {}
        for col_name, entry_id in ID_MAP.items():
            # Ensure all values are converted to string for the request
            payload[entry_id] = str(row[col_name])
            
        # 2. Submit the payload
        try:
            response = requests.post(URL, data=payload)
            
            # 3. Log the result
            if response.status_code == 200:
                print(f"✅ Record {index + 1}/{total_records} submitted successfully. Status: 200")
            else:
                print(f"❌ Record {index + 1}/{total_records} FAILED. Status: {response.status_code}. Pausing for a longer time.")
                time.sleep(30) # Longer pause on failure
                continue 

        except requests.exceptions.RequestException as e:
            print(f"❌ Record {index + 1}/{total_records} FAILED due to connection error: {e}")
            time.sleep(30)
            continue

        # 4. Wait for the defined interval
        time.sleep(SUBMISSION_DELAY_SECONDS)
        print(f"--- Paused for {SUBMISSION_DELAY_SECONDS} seconds ---")


    print("\n--- Submission process complete for this batch. ---")

# --- Main Execution ---
if __name__ == "__main__":
    # 0. Check for dependencies first (critical for GitHub Actions)
    try:
        import pandas as pd
    except ImportError:
        print("❌ Error: The 'pandas' library is required. Please install it with 'pip install pandas'")
        sys.exit(1)

    # 1. Get the starting index from command line arguments (default to 0)
    try:
        start_index = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    except ValueError:
        print("Invalid starting index provided. Using default index 0.")
        start_index = 0
        
    # 2. Ensure the CSV is generated (will only run if the file is missing)
    # The number of records for generation is hardcoded to NUM_RECORDS
    generate_csv(NUM_RECORDS)
    
    # 3. Submit the data starting from the specified index
    submit_from_csv(start_index)
