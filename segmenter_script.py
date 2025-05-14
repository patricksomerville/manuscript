#!/usr/bin/env python3
import json
import re
import argparse
import os

# Basic keyword lists for heuristic tagging (can be expanded significantly)
DIALOGUE_VERBS = ["said", "asked", "replied", "exclaimed", "whispered", "muttered", "shouted", "cried", "gasped"]
INTERIOR_STATE_VERBS = ["thought", "felt", "wondered", "realized", "knew", "remembered", "imagined", "considered"]
DESCRIPTION_ADJECTIVES = ["beautiful", "dark", "vast", "tiny", "old", "new", "red", "blue", "cold", "warm"] # Example

SATIRICAL_KEYWORDS = ["bureaucracy", "corporate", "hero", "engineer", "mech", "manual", "cost-cutting", "marketing-driven"]
HUMOROUS_KEYWORDS = ["funny", "laugh", "joke", "ridiculous", "absurd"]

# Simplified character list for example (in a real system, this would be managed externally)
KNOWN_CHARACTERS = ["Hanson", "FLANT", "Vance", "Director Thorne"]

def identify_characters_in_text(text, known_chars):
    present_chars = []
    for char_name in known_chars:
        if re.search(r'\b' + re.escape(char_name) + r'\b', text, re.IGNORECASE):
            present_chars.append(char_name)
    return present_chars

def segment_chapter(chapter_text, chapter_id):
    """Segments chapter text into paragraphs and assigns granular tags based on revised schema."""
    segments = []
    # Split by one or more newline characters, effectively treating paragraphs as segments
    paragraphs = re.split(r'\n\s*\n+', chapter_text.strip())
    
    for i, para_text in enumerate(paragraphs):
        text_to_analyze = para_text.strip()
        if not text_to_analyze:
            continue
        
        segment = {
            "SegmentID": f"{chapter_id}_SEG{i+1:05d}",
            "SegmentOrder": i + 1,
            "SegmentText": text_to_analyze,
            "PrimaryNarrativeMode": "Narration-Action", # Default
            "SecondaryNarrativeModes": [],
            "DialogueSpeaker": None,
            "DialogueAddressees": [],
            "DialogueContext": None,
            "DialogueTone": [],
            "PlotFunctionTags": [],
            "MysteryTags": [],
            "CharacterArcTags": [],
            "WorldBuildingTags": [],
            "StructuralOntologyTags": [],
            "AuthorialIntentTags": [],
            "ThematicKeywordsRaw": "", # Placeholder, could be extracted with NLP
            "CharactersInSegment": identify_characters_in_text(text_to_analyze, KNOWN_CHARACTERS),
            "CharacterPOVHolder": None, # Complex to determine automatically
            "LocationInSegment": None, # Placeholder, requires context or NLP
            "TimeReferenceInSegment": None, # Placeholder, requires context or NLP
            "ClueReferenceInSegment": [],
            "SegmentNotes": "Initial granular segmentation."
        }

        # --- Heuristic Tagging Logic ---

        # 1. Primary Narrative Mode & Dialogue details
        is_dialogue = False
        dialogue_match = re.match(r'^["“](.*?)["”](?:\s*(\w+)\s*(?:to\s*(\w+))?\s*(said|asked|replied|exclaimed|whispered|muttered|shouted|cried|gasped))?', text_to_analyze, re.IGNORECASE)
        if dialogue_match:
            is_dialogue = True
            segment["PrimaryNarrativeMode"] = "Dialogue"
            #dialogue_content = dialogue_match.group(1)
            speaker_candidate = dialogue_match.group(2)
            #addressee_candidate = dialogue_match.group(3) # Often not present
            #verb = dialogue_match.group(4)
            if speaker_candidate and speaker_candidate in KNOWN_CHARACTERS:
                 segment["DialogueSpeaker"] = speaker_candidate
            # Basic tone based on verb (very simplistic)
            # if verb in ["shouted", "exclaimed"]: segment["DialogueTone"].append("Emotional") 

        elif any(verb in text_to_analyze.lower() for verb in DIALOGUE_VERBS) and (text_to_analyze.count('"') >= 2 or text_to_analyze.count('“') >=2 ):
             is_dialogue = True # Likely dialogue even if not matching the simple regex
             segment["PrimaryNarrativeMode"] = "Dialogue"

        if not is_dialogue:
            if any(verb in text_to_analyze.lower() for verb in INTERIOR_STATE_VERBS):
                segment["PrimaryNarrativeMode"] = "Narration-InteriorState"
            elif len(text_to_analyze.split()) > 20 and any(adj in text_to_analyze.lower() for adj in DESCRIPTION_ADJECTIVES): # Arbitrary length for description
                segment["PrimaryNarrativeMode"] = "Narration-Description"
            elif text_to_analyze.isupper() and len(text_to_analyze.split()) < 10: # Heuristic for e.g. location/time headers
                segment["PrimaryNarrativeMode"] = "Meta-Narration"
                segment["StructuralOntologyTags"].append("TimeMarkerExplicit" if re.search(r'\b(day|night|morning|evening|hour|minute|monday|tuesday|january|february)\b', text_to_analyze, re.IGNORECASE) else "LocationMarkerExplicit")
            # Default is Narration-Action or Narration-Exposition (hard to distinguish simply)

        # 2. Authorial Intent Tags (from narrative_design.md concepts)
        if any(keyword in text_to_analyze.lower() for keyword in SATIRICAL_KEYWORDS):
            segment["AuthorialIntentTags"].append("SatiricalElement")
        if any(keyword in text_to_analyze.lower() for keyword in HUMOROUS_KEYWORDS):
            segment["AuthorialIntentTags"].append("HumorousElement")

        # 3. Mystery Tags (Example)
        if "clue" in text_to_analyze.lower() or "evidence" in text_to_analyze.lower():
            segment["MysteryTags"].append("ClueDeployment") # Could be analysis too
        if "detective" in text_to_analyze.lower() or "investigation" in text_to_analyze.lower():
            segment["MysteryTags"].append("DeductionByCharacter")

        # 4. Structural Ontology Tags (from narrative_ontology.py concepts - very basic examples)
        if re.search(r'\b(because|therefore|thus|as a result)\b', text_to_analyze, re.IGNORECASE):
            segment["StructuralOntologyTags"].append("CausalLink-Consequence")
        if re.search(r'\b(previously|earlier|before that|remembered when)\b', text_to_analyze, re.IGNORECASE):
            segment["StructuralOntologyTags"].append("FlashbackMarker")

        # 5. WorldBuilding Tags
        if "Aethelburg" in text_to_analyze or "Neo-London" in text_to_analyze: # Example locations
            segment["WorldBuildingTags"].append("SettingDescriptionPhysical")
            if not segment["LocationInSegment"]:
                 segment["LocationInSegment"] = text_to_analyze # Simplistic assignment

        # 6. Character Arc Tags
        if segment["PrimaryNarrativeMode"] == "Narration-InteriorState" and segment["CharactersInSegment"]:
            segment["CharacterArcTags"].append("InternalStruggleDemonstrated")
        if is_dialogue and len(segment["CharactersInSegment"]) >=2:
            segment["CharacterArcTags"].append("RelationshipDevelopment") # or conflict

        # 7. Plot Function Tags
        # These are very hard to automate without full plot understanding. Placeholder.
        if i < 5 and chapter_id.endswith("01"): # First few segments of first chapter
            segment["PlotFunctionTags"].append("IncitingIncident") # Highly speculative

        # Remove duplicates from tag lists
        for key in segment:
            if isinstance(segment[key], list):
                segment[key] = sorted(list(set(segment[key])))

        segments.append(segment)
    return segments

def main():
    parser = argparse.ArgumentParser(description="Segment a novel chapter into text segments and apply granular tags.")
    parser.add_argument("input_file", help="Path to the input chapter text file (.md or .txt)")
    parser.add_argument("output_file", help="Path to the output JSON file for segmented data")
    parser.add_argument("chapter_id", help="Unique ID for the chapter (e.g., CH001)")
    
    args = parser.parse_args()
    
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            chapter_content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file {args.input_file} not found.")
        return
    except Exception as e:
        print(f"Error reading input file: {e}")
        return
        
    segmented_data = segment_chapter(chapter_content, args.chapter_id)
    
    chapter_output = {
        "ChapterID": args.chapter_id,
        "Segments": segmented_data
    }
    
    try:
        os.makedirs(os.path.dirname(args.output_file), exist_ok=True)
        with open(args.output_file, 'w', encoding='utf-8') as f:
            json.dump(chapter_output, f, indent=4, ensure_ascii=False)
        print(f"Successfully segmented chapter {args.chapter_id} and saved to {args.output_file}")
    except Exception as e:
        print(f"Error writing output file: {e}")

if __name__ == "__main__":
    main()

