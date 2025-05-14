import json
import argparse

def get_chapter_segments(chapter_id_to_find, chapters_file, segments_file):
    """Extracts and orders segments for a specific chapter."""
    try:
        with open(chapters_file, 'r') as f:
            chapters_data = json.load(f)
        with open(segments_file, 'r') as f:
            segments_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: One or both data files not found ({chapters_file}, {segments_file})")
        return None, None, 0, 0
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from one or both data files.")
        return None, None, 0, 0

    target_chapter_record_id = None
    chapter_title = "Unknown Chapter"
    current_word_count = 0

    for chapter in chapters_data:
        if chapter.get('fields', {}).get('Chapter ID') == chapter_id_to_find:
            target_chapter_record_id = chapter.get('id')
            chapter_title = chapter.get('fields', {}).get('Chapter Title', chapter_id_to_find)
            current_word_count = chapter.get('fields', {}).get('Word Count', 0)
            break

    if not target_chapter_record_id:
        print(f"Error: Chapter with ID '{chapter_id_to_find}' not found in {chapters_file}")
        return None, None, 0, 0

    chapter_segments = []
    for segment in segments_data:
        if segment.get('fields', {}).get('Chapter Link') and target_chapter_record_id in segment.get('fields', {}).get('Chapter Link'):
            chapter_segments.append(segment)
    
    chapter_segments.sort(key=lambda s: s.get('fields', {}).get('Segment Order', float('inf')))
    
    full_text = "\n\n".join([s.get('fields', {}).get('Segment Text', '') for s in chapter_segments])
    
    return chapter_title, full_text, current_word_count, len(chapter_segments)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Assemble chapter text from Airtable data.")
    parser.add_argument("-c", "--chapter_id", type=str, default="CH001", help="Chapter ID to assemble (e.g., CH001)")
    args = parser.parse_args()

    chapter_id_to_assemble = args.chapter_id
    chapters_json_path = '/home/ubuntu/novel_project/airtable_chapters_data.json'
    segments_json_path = '/home/ubuntu/novel_project/airtable_segments_data.json'
    output_dir = "/home/ubuntu/novel_project/"

    title, text, words, num_segments = get_chapter_segments(chapter_id_to_assemble, chapters_json_path, segments_json_path)
    
    if title and text is not None: # Ensure text is not None, even if empty
        print(f"--- Chapter: {title} ---")
        print(f"Current Word Count (from Airtable): {words}")
        print(f"Number of Segments: {num_segments}")
        
        output_filename = f"{output_dir}{chapter_id_to_assemble}_current_text.md"
        with open(output_filename, "w") as f_out:
            f_out.write(f"# {title}\n\nWord Count (Airtable): {words}\nSegments: {num_segments}\n\n")
            f_out.write(text)
        print(f"Saved current text of {chapter_id_to_assemble} to {output_filename}")
    else:
        print(f"Could not retrieve text for {chapter_id_to_assemble}")

