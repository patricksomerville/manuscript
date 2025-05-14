#!/usr/bin/env python3
import json
import os
import argparse
import time
from airtable import Airtable

# Helper function to handle potentially long text fields for Airtable
# Airtable has a limit of 100,000 characters for long text fields.
def truncate_text(text, limit=99900):
    if len(text) > limit:
        return text[:limit] + "... (truncated)"
    return text

# Helper to convert list to comma-separated string for certain Airtable fields if needed
# Or ensure it's a list for multi-select
def format_for_airtable(value):
    if isinstance(value, list):
        # For multi-select fields, Airtable Python wrapper expects a list of strings
        return [str(v) for v in value]
    return value

def upload_to_airtable(api_key, base_id, chapters_table_name, segments_table_name, staging_dir):
    """Uploads segmented chapter data to Airtable."""
    
    airtable_chapters = Airtable(base_id, chapters_table_name, api_key)
    airtable_segments = Airtable(base_id, segments_table_name, api_key)
    
    processed_chapters = 0
    processed_segments = 0

    print(f"Starting upload from {staging_dir}...")

    for filename in sorted(os.listdir(staging_dir)):
        if filename.endswith("_segmented_granular.json"):
            filepath = os.path.join(staging_dir, filename)
            print(f"Processing file: {filepath}")
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                continue

            chapter_id_from_file = data.get("ChapterID", "UnknownChapter")
            chapter_number_str = chapter_id_from_file.replace("CH", "")
            try:
                chapter_number = int(chapter_number_str)
            except ValueError:
                chapter_number = 0 # Or handle error appropriately
                print(f"Warning: Could not parse chapter number from {chapter_id_from_file}")

            # 1. Create/Update Chapter Record
            # For simplicity, this script assumes chapter records are new or can be identified uniquely by ChapterID.
            # A more robust solution would check if a record with ChapterID exists and update it.
            
            # Calculate total word count for the chapter from its segments
            chapter_word_count = 0
            if data.get("Segments"):
                for seg in data["Segments"]:
                    chapter_word_count += len(seg.get("SegmentText", "").split())

            chapter_data = {
                "Chapter ID": chapter_id_from_file,
                "Chapter Number": chapter_number,
                "Chapter Title": f"Chapter {chapter_number_str} (Title Placeholder)", # Placeholder
                "Chapter Status": "Uploaded to Airtable",
                "Word Count": chapter_word_count,
                # "Synopsis": "Synopsis placeholder...", # Add if available
                # "CharactersAppearing": [], # Link to Characters table - requires existing character records
                # "PrimaryThemes": [], # Link to Themes table
            }
            
            try:
                # Check if chapter exists
                existing_chapter = airtable_chapters.match("Chapter ID", chapter_id_from_file)
                if existing_chapter:
                    print(f"Chapter {chapter_id_from_file} already exists. Record ID: {existing_chapter['id']}. Skipping chapter creation.")
                    chapter_record_id = existing_chapter['id']
                else:
                    created_chapter = airtable_chapters.insert(chapter_data)
                    print(f"Created Chapter record for {chapter_id_from_file}: {created_chapter['id']}")
                    chapter_record_id = created_chapter['id']
                processed_chapters += 1
            except Exception as e:
                print(f"Error creating/finding chapter record for {chapter_id_from_file}: {e}")
                continue # Skip segments if chapter creation failed

            # 2. Create Segment Records
            segments_to_upload_batch = []
            for seg_data in data.get("Segments", []):
                airtable_segment_data = {
                    "Segment ID": seg_data.get("SegmentID"),
                    "Chapter Link": [chapter_record_id], # Link to the chapter record
                    "Segment Order": seg_data.get("SegmentOrder"),
                    "Segment Text": truncate_text(seg_data.get("SegmentText")),
                    "Narrative Mode": seg_data.get("PrimaryNarrativeMode"),
                    "SecondaryNarrativeModes": format_for_airtable(seg_data.get("SecondaryNarrativeModes")),
                    # "DialogueSpeaker": [], # Link to Characters - needs existing record ID
                    # "DialogueAddressees": [], # Link to Characters
                    "DialogueContext": seg_data.get("DialogueContext"),
                    "DialogueTone": format_for_airtable(seg_data.get("DialogueTone")),
                    "PlotFunctionTags": format_for_airtable(seg_data.get("PlotFunctionTags")),
                    "MysteryTags": format_for_airtable(seg_data.get("MysteryTags")),
                    "CharacterArcTags": format_for_airtable(seg_data.get("CharacterArcTags")),
                    "WorldBuildingTags": format_for_airtable(seg_data.get("WorldBuildingTags")),
                    "StructuralOntologyTags": format_for_airtable(seg_data.get("StructuralOntologyTags")),
                    "AuthorialIntentTags": format_for_airtable(seg_data.get("AuthorialIntentTags")),
                    "ThematicKeywordsRaw": seg_data.get("ThematicKeywordsRaw"),
                    # "CharactersInSegment": [], # Link to Characters
                    # "CharacterPOVHolder": [], # Link to Characters
                    "LocationInSegment": seg_data.get("LocationInSegment"), # Assumes text for now
                    "TimeReferenceInSegment": seg_data.get("TimeReferenceInSegment"),
                    # "ClueReferenceInSegment": [], # Link to Clues
                    "SegmentNotes": truncate_text(seg_data.get("SegmentNotes")),
                }
                
                # Filter out None values, as Airtable API might not like them for certain field types
                # For linked records, empty lists are fine. For single/multi-select, None might be an issue.
                # It's safer to omit the key if the value is None and the field is not required.
                final_segment_data = {k: v for k, v in airtable_segment_data.items() if v is not None and v != []}
                segments_to_upload_batch.append(final_segment_data)

                if len(segments_to_upload_batch) == 10: # Airtable batch limit is 10
                    try:
                        airtable_segments.batch_insert(segments_to_upload_batch)
                        print(f"Uploaded batch of {len(segments_to_upload_batch)} segments for {chapter_id_from_file}.")
                        processed_segments += len(segments_to_upload_batch)
                    except Exception as e:
                        print(f"Error batch inserting segments for {chapter_id_from_file}: {e}")
                        # Optionally, try inserting one by one for debugging
                        # for single_seg_data in segments_to_upload_batch:
                        #     try: airtable_segments.insert(single_seg_data)
                        #     except Exception as e_single: print(f"Error single: {e_single}")
                    segments_to_upload_batch = []
                    time.sleep(1) # Basic rate limiting
            
            if segments_to_upload_batch: # Upload any remaining segments
                try:
                    airtable_segments.batch_insert(segments_to_upload_batch)
                    print(f"Uploaded final batch of {len(segments_to_upload_batch)} segments for {chapter_id_from_file}.")
                    processed_segments += len(segments_to_upload_batch)
                except Exception as e:
                    print(f"Error batch inserting final segments for {chapter_id_from_file}: {e}")
                time.sleep(1)

    print(f"Upload complete. Processed {processed_chapters} chapters and {processed_segments} segments.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload segmented novel data to Airtable.")
    parser.add_argument("--api_key", required=True, help="Airtable API Key")
    parser.add_argument("--base_id", required=True, help="Airtable Base ID")
    parser.add_argument("--chapters_table", required=True, help="Name of the Chapters table in Airtable")
    parser.add_argument("--segments_table", required=True, help="Name of the Text Segments table in Airtable")
    parser.add_argument("--staging_dir", default="/home/ubuntu/novel_project/airtable_staging/", help="Directory containing the _segmented_granular.json files")
    
    args = parser.parse_args()
    
    # It's good practice to ensure the Airtable library is installed.
    # This script assumes it is. If not: pip install airtable-python-wrapper
    
    upload_to_airtable(args.api_key, args.base_id, args.chapters_table, args.segments_table, args.staging_dir)

