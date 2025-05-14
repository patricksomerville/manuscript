#!/usr/bin/env python3
import json
import os
from collections import defaultdict

def extract_multiselect_options(staging_dir):
    """Extracts all unique options for predefined multi-select fields from JSON files."""
    
    # These are the keys in the JSON that correspond to multi-select fields in Airtable
    # as per the airtable_uploader.py script logic.
    multi_select_fields = [
        "SecondaryNarrativeModes",
        "DialogueTone",
        "PlotFunctionTags",
        "MysteryTags",
        "CharacterArcTags",
        "WorldBuildingTags",
        "StructuralOntologyTags",
        "AuthorialIntentTags"
    ]
    
    all_options = defaultdict(set)

    print(f"Scanning files in {staging_dir} for multi-select options...")

    for filename in sorted(os.listdir(staging_dir)):
        if filename.endswith("_segmented_granular.json"):
            filepath = os.path.join(staging_dir, filename)
            # print(f"Processing file: {filepath}")
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                continue

            segments = data.get("Segments", [])
            for seg_data in segments:
                for field_name in multi_select_fields:
                    field_values = seg_data.get(field_name)
                    if field_values:
                        # Ensure it's a list, as some might be single strings if not properly formatted in source
                        if isinstance(field_values, list):
                            for value in field_values:
                                if value and isinstance(value, str):
                                    all_options[field_name].add(value.strip())
                        elif isinstance(field_values, str): # Handle if it's a single string by mistake
                             if field_values:
                                all_options[field_name].add(field_values.strip())
                                
    # Prepare the output report
    report_lines = ["# Required Options for Airtable Multiple Select Fields\n"]
    report_lines.append("Please ensure the following options are created in your Airtable 'Text Segments' table for the respective Multiple Select fields:\n")
    
    for field, options_set in all_options.items():
        if options_set:
            report_lines.append(f"## Field: {field}\n")
            for option in sorted(list(options_set)):
                report_lines.append(f"- {option}\n")
            report_lines.append("\n")
        else:
            report_lines.append(f"## Field: {field}\n")
            report_lines.append("- (No options found in data for this field)\n\n")
            
    output_filepath = "/home/ubuntu/novel_project/required_airtable_multiselect_options.md"
    with open(output_filepath, 'w', encoding='utf-8') as f_out:
        f_out.write("\n".join(report_lines))
        
    print(f"Successfully extracted options. Report saved to: {output_filepath}")
    return output_filepath

if __name__ == "__main__":
    staging_directory = "/home/ubuntu/novel_project/airtable_staging/"
    report_file = extract_multiselect_options(staging_directory)
    # The script will print the path to the report, which can then be used by the agent.

