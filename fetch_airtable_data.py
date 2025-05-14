import os
import requests
import json

AIRTABLE_API_KEY = "patLp1BLsnVXKuiQq.73e184272c8f175f6b3383eb3e61ea6edb70dff2db38858f6b387266cc861868"
AIRTABLE_BASE_ID = "appYaxSciZz3FHgaV"
CHAPTERS_TABLE_NAME = "Chapters"
TEXT_SEGMENTS_TABLE_NAME = "Text Segments"

OUTPUT_CHAPTERS_FILE = "/home/ubuntu/novel_project/airtable_chapters_data.json"
OUTPUT_SEGMENTS_FILE = "/home/ubuntu/novel_project/airtable_segments_data.json"

headers = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
}

def fetch_all_records(base_id, table_name):
    records = []
    url = f"https://api.airtable.com/v0/{base_id}/{table_name}"
    params = {}

    while True:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        records.extend(data.get("records", []))
        offset = data.get("offset")
        if not offset:
            break
        params["offset"] = offset
    return records

def main():
    print(f"Fetching records from Chapters table: {CHAPTERS_TABLE_NAME}...")
    try:
        chapter_records = fetch_all_records(AIRTABLE_BASE_ID, CHAPTERS_TABLE_NAME)
        with open(OUTPUT_CHAPTERS_FILE, "w") as f:
            json.dump(chapter_records, f, indent=4)
        print(f"Successfully fetched {len(chapter_records)} records from Chapters table and saved to {OUTPUT_CHAPTERS_FILE}")
    except requests.exceptions.HTTPError as e:
        print(f"Error fetching Chapters data: {e}")
        if e.response.status_code == 401:
            print("Airtable API Key is likely invalid or expired. Please check.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while fetching Chapters data: {e}")
        return

    print(f"Fetching records from Text Segments table: {TEXT_SEGMENTS_TABLE_NAME}...")
    try:
        segment_records = fetch_all_records(AIRTABLE_BASE_ID, TEXT_SEGMENTS_TABLE_NAME)
        with open(OUTPUT_SEGMENTS_FILE, "w") as f:
            json.dump(segment_records, f, indent=4)
        print(f"Successfully fetched {len(segment_records)} records from Text Segments table and saved to {OUTPUT_SEGMENTS_FILE}")
    except requests.exceptions.HTTPError as e:
        print(f"Error fetching Text Segments data: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while fetching Text Segments data: {e}")

if __name__ == "__main__":
    main()
