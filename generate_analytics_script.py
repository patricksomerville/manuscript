#!/usr/bin/env python3
import json
import os
from collections import Counter, defaultdict

def generate_airtable_summary_analytics(staging_dir):
    """Generates summary analytics from the segmented JSON files."""
    
    total_segments_processed = 0
    segments_per_chapter = defaultdict(int)
    
    # Counters for various tags
    narrative_mode_counts = Counter()
    secondary_narrative_modes_counts = Counter()
    plot_function_tags_counts = Counter()
    mystery_tags_counts = Counter()
    character_arc_tags_counts = Counter()
    world_building_tags_counts = Counter()
    structural_ontology_tags_counts = Counter()
    authorial_intent_tags_counts = Counter()
    dialogue_context_counts = Counter()
    dialogue_tone_counts = Counter()
    location_counts = Counter()
    time_reference_counts = Counter()

    # Explicit mapping from field names in JSON to Counter objects
    multi_select_field_to_counter_map = {
        "SecondaryNarrativeModes": secondary_narrative_modes_counts,
        "DialogueTone": dialogue_tone_counts,
        "PlotFunctionTags": plot_function_tags_counts,
        "MysteryTags": mystery_tags_counts,
        "CharacterArcTags": character_arc_tags_counts,
        "WorldBuildingTags": world_building_tags_counts,
        "StructuralOntologyTags": structural_ontology_tags_counts,
        "AuthorialIntentTags": authorial_intent_tags_counts
    }

    print(f"Generating analytics from files in {staging_dir}...")

    for filename in sorted(os.listdir(staging_dir)):
        if filename.endswith("_segmented_granular.json"):
            filepath = os.path.join(staging_dir, filename)
            chapter_id = filename.replace("_segmented_granular.json", "").replace("chapter_", "CH").upper()
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                continue

            segments = data.get("Segments", [])
            segments_per_chapter[chapter_id] += len(segments)
            total_segments_processed += len(segments)
            
            for seg_data in segments:
                # Narrative Mode (Single Select)
                nm = seg_data.get("Narrative Mode")
                if nm: narrative_mode_counts[nm] += 1
                
                # Location & Time
                loc = seg_data.get("LocationInSegment")
                if loc: location_counts[loc] +=1
                time_ref = seg_data.get("TimeReferenceInSegment")
                if time_ref: time_reference_counts[time_ref] += 1

                # Dialogue Specific (Single Select or Text)
                dc = seg_data.get("DialogueContext")
                if dc: dialogue_context_counts[dc] += 1

                # Multi-select fields
                for field_name, counter_to_update in multi_select_field_to_counter_map.items():
                    field_values = seg_data.get(field_name)
                    if field_values:
                        if isinstance(field_values, list):
                            for value in field_values:
                                if value and isinstance(value, str):
                                    counter_to_update[value.strip()] += 1
                        elif isinstance(field_values, str):
                            if field_values:
                                counter_to_update[field_values.strip()] += 1
                                
    # Prepare the report
    report_lines = ["# Airtable Data Summary Analytics\n"]
    report_lines.append(f"Generated on: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
    report_lines.append(f"Total Segments Processed from JSON files: {total_segments_processed}\n")
    
    report_lines.append("## Segments per Chapter\n")
    for ch_id, count in sorted(segments_per_chapter.items()):
        report_lines.append(f"- {ch_id}: {count} segments\n")
    report_lines.append("\n")

    def add_counter_to_report(title, counter):
        report_lines.append(f"## {title}\n")
        if counter:
            for item, count in counter.most_common():
                report_lines.append(f"- {item}: {count}\n")
        else:
            report_lines.append("- No data found for this category.\n")
        report_lines.append("\n")

    add_counter_to_report("Narrative Mode Distribution", narrative_mode_counts)
    add_counter_to_report("Secondary Narrative Modes Distribution", secondary_narrative_modes_counts)
    add_counter_to_report("Plot Function Tags Distribution", plot_function_tags_counts)
    add_counter_to_report("Mystery Tags Distribution", mystery_tags_counts)
    add_counter_to_report("Character Arc Tags Distribution", character_arc_tags_counts)
    add_counter_to_report("World Building Tags Distribution", world_building_tags_counts)
    add_counter_to_report("Structural Ontology Tags Distribution", structural_ontology_tags_counts)
    add_counter_to_report("Authorial Intent Tags Distribution", authorial_intent_tags_counts)
    add_counter_to_report("Dialogue Context Distribution", dialogue_context_counts)
    add_counter_to_report("Dialogue Tone Distribution", dialogue_tone_counts)
    add_counter_to_report("Location Mentions in Segments", location_counts)
    add_counter_to_report("Time References in Segments", time_reference_counts)
            
    output_filepath = "/home/ubuntu/novel_project/airtable_summary_analytics.md"
    with open(output_filepath, 'w', encoding='utf-8') as f_out:
        f_out.write("\n".join(report_lines))
        
    print(f"Successfully generated analytics. Report saved to: {output_filepath}")
    return output_filepath

if __name__ == "__main__":
    staging_directory = "/home/ubuntu/novel_project/airtable_staging/"
    report_file = generate_airtable_summary_analytics(staging_directory)
    # The script will print the path to the report, which can then be used by the agent.

