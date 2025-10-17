# Manuscript Workflow - Quick Start Guide

## What This Is

The Manuscript Workflow System is a command-line tool for managing novel-length narratives using a structured database (Airtable), Python scripts, and AI-driven analysis.

## Installation

```bash
# Clone or navigate to the manuscript directory
cd manuscript

# Run the installation script
./install.sh

# Add to PATH (if needed)
export PATH="$HOME/.local/bin:$PATH"
```

## Quick Start

### 1. Initialize Your Project

```bash
manuscript init \
  --airtable-key YOUR_AIRTABLE_API_KEY \
  --airtable-base YOUR_AIRTABLE_BASE_ID \
  --output-dir ./output
```

This creates a configuration file at `~/.manuscript/config.json` with your settings.

### 2. Check Project Status

```bash
manuscript status
```

Shows your current configuration and output files.

### 3. Segment a Chapter

```bash
# Basic usage
manuscript segment chapter01.txt CH001

# Specify output file
manuscript segment chapter01.txt CH001 -o output/ch001_segments.json
```

This breaks your chapter into segments and applies AI-ready tags for:
- Narrative mode (dialogue, action, description, interior state)
- Character presence and POV
- Plot function
- Mystery elements
- Thematic keywords
- Structural markers

### 4. Upload to Airtable

```bash
manuscript upload output/ch001_segments.json
```

Sends your segmented data to Airtable for collaborative editing and AI analysis.

### 5. Fetch from Airtable

```bash
# Fetch all data
manuscript fetch

# Specify output directory
manuscript fetch -o ./airtable_data
```

Downloads your Airtable data for local processing.

### 6. Assemble a Chapter

```bash
manuscript assemble CH001 -o assembled_chapter01.md
```

Reconstructs a chapter from Airtable segments.

### 7. Generate Analytics

```bash
manuscript analytics -o analytics_report.json
```

Creates quantitative analysis of your manuscript:
- Word counts per chapter/segment
- Character appearance frequency
- Narrative mode distribution
- Tag statistics

## Workflow Example

Here's a complete workflow for processing a novel:

```bash
# 1. Initialize project
manuscript init --airtable-key $AIRTABLE_KEY --airtable-base $AIRTABLE_BASE

# 2. Segment all chapters
for chapter in chapters/*.txt; do
    chapter_id=$(basename "$chapter" .txt | tr '[:lower:]' '[:upper:]')
    manuscript segment "$chapter" "$chapter_id"
done

# 3. Upload all segments to Airtable
for segment_file in output/*_segments.json; do
    manuscript upload "$segment_file"
done

# 4. Work in Airtable (AI analysis, tagging, editing)
# ... time passes ...

# 5. Fetch updated data
manuscript fetch

# 6. Generate analytics
manuscript analytics -o manuscript_analytics.json

# 7. Assemble final chapters
manuscript assemble CH001 -o final/chapter01.md
manuscript assemble CH002 -o final/chapter02.md
```

## Configuration

The configuration file is stored at `~/.manuscript/config.json`:

```json
{
  "airtable_api_key": "your_key_here",
  "airtable_base_id": "your_base_id_here",
  "default_output_dir": "/path/to/output",
  "known_characters": ["Hanson", "FLANT", "Vance"]
}
```

You can edit this file directly or use `manuscript init` to update it.

## Environment Variables

Alternatively, you can use environment variables:

```bash
export AIRTABLE_API_KEY="your_key"
export AIRTABLE_BASE_ID="your_base"
export AIRTABLE_CHAPTERS_TABLE_ID="tblXXXXXX"
export AIRTABLE_SEGMENTS_TABLE_ID="tblYYYYYY"
```

## Tips & Best Practices

### Segmentation

- **Paragraph-level**: The default segmentation treats each paragraph as a segment
- **Custom characters**: Edit the config to add your novel's characters for better tagging
- **Manual review**: Always review auto-generated tags in Airtable

### Airtable Schema

See `novel_project_airtable_schema.md` for the complete database schema.

Key tables:
- **Chapters**: High-level chapter metadata
- **Text Segments**: Individual paragraphs with granular tags
- **Characters**: Character database
- **Locations**: Setting database
- **Plot Points**: Story structure tracking

### AI Integration

The system is designed to work with AI agents (like Manus) for:
- Automated tagging and analysis
- Context-aware editing suggestions
- Thematic analysis
- Character arc tracking

### Version Control

Keep your segmented JSON files in git:

```bash
git add output/*.json
git commit -m "Segmented chapters 1-5"
```

This provides a backup and change history independent of Airtable.

## Troubleshooting

### Command not found: manuscript

Add `~/.local/bin` to your PATH:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Airtable authentication errors

1. Check your API key is valid
2. Verify your base ID is correct
3. Ensure you have write permissions to the base

### Python dependency errors

Install dependencies manually:

```bash
pip3 install --user requests python-dotenv
```

## Next Steps

- Read `proprietary_novel_generation_workflow.md` for the complete system architecture
- Review `novel_project_airtable_schema.md` for database design
- Explore the individual Python scripts for advanced customization

## Support

This is a proprietary system developed by Patrick Somerville with assistance from the Manus AI agent.

For questions or issues, refer to the documentation in this repository.

