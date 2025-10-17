# Manuscript Workflow System

A proprietary workflow system for the generation, expansion, and management of novel-length narratives.

## What's New

**✨ Version 2.0 - Unified CLI Interface**

The manuscript workflow now includes a unified command-line interface (`manuscript`) that simplifies all operations.

```bash
# Install the CLI
./install.sh

# Initialize your project
manuscript init --airtable-key YOUR_KEY --airtable-base YOUR_BASE

# Segment a chapter
manuscript segment chapter01.txt CH001

# Check status
manuscript status
```

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions.

This repository contains the codebase and documentation for a proprietary workflow designed for the generation, expansion, and management of novel-length narratives. The system leverages a combination of a structured database (Airtable), custom Python scripts for data processing and automation, AI-driven content generation and analysis (facilitated by an AI agent like Manus), and iterative user guidance through prompts and feedback.

## Overview

The core idea is to create a flexible yet robust framework that can support the creation of complex narratives from initial concept to a complete manuscript, allowing for detailed tracking, targeted development, and data-informed creative decisions.

Refer to `proprietary_novel_generation_workflow.md` for a detailed breakdown of the system architecture, components, and workflow steps.

## Components

*   **Airtable**: Central narrative database. Schema details in `novel_project_airtable_schema.md`.
*   **Python Scripts**: Located in the root of this repository. These scripts handle tasks such as text segmentation, Airtable uploading/fetching, chapter assembly, and analytics generation.
*   **CLI Tool**: `manuscript_cli.py` - Unified interface for all operations (new!)
*   **Workflow Documentation**: `proprietary_novel_generation_workflow.md`.

## Installation

### Quick Install

```bash
./install.sh
```

This will:
- Install Python dependencies from `requirements.txt`
- Create a `manuscript` command in `~/.local/bin`
- Set up the configuration structure

### Manual Installation

1. Install Python 3.11+
2. Install dependencies: `pip3 install -r requirements.txt`
3. Make CLI executable: `chmod +x manuscript_cli.py`
4. Create symlink: `ln -s $(pwd)/manuscript_cli.py ~/.local/bin/manuscript`

## Setup

1.  **Airtable**: 
    *   Set up an Airtable base according to the schema defined in `novel_project_airtable_schema.md`.
    *   Obtain your Airtable API Key and Base ID.
2.  **Initialize Project**:
    ```bash
    manuscript init \
      --airtable-key YOUR_AIRTABLE_API_KEY \
      --airtable-base YOUR_AIRTABLE_BASE_ID \
      --output-dir ./output
    ```
3.  **Environment Variables** (Alternative): The Python scripts can also use environment variables:
    *   `AIRTABLE_API_KEY`: Your Airtable Personal Access Token.
    *   `AIRTABLE_BASE_ID`: The ID of your Airtable base for the novel project.
    *   `AIRTABLE_CHAPTERS_TABLE_ID`: The ID of the "Chapters" table in your base.
    *   `AIRTABLE_SEGMENTS_TABLE_ID`: The ID of the "Text Segments" table in your base.

## Scripts

*   `segmenter_script.py`: Processes initial manuscript text into segments.
*   `airtable_uploader.py`: Uploads segmented text to Airtable.
*   `fetch_airtable_data.py`: Fetches data from Airtable to local JSON files.
*   `extract_options_script.py`: Manages options for multi-select fields in Airtable.
*   `chapter_assembler.py`: Assembles chapter text from Airtable segments.
*   `generate_analytics_script.py`: Generates quantitative analytics from Airtable data.

## Usage

### CLI Commands

```bash
manuscript init        # Initialize project configuration
manuscript segment     # Segment a chapter into tagged paragraphs
manuscript upload      # Upload segments to Airtable
manuscript fetch       # Fetch data from Airtable
manuscript assemble    # Assemble chapter from segments
manuscript analytics   # Generate quantitative analytics
manuscript status      # Show project status
```

See [QUICKSTART.md](QUICKSTART.md) for detailed examples and workflows.

### Individual Scripts (Legacy)

The individual Python scripts can still be used directly. Refer to the scripts and the main workflow document for detailed usage instructions. The system is designed to be orchestrated by an AI agent (like Manus) or run manually by a user familiar with the components.

## Future Development

This system is intended for ongoing development. Future enhancements may include:

*   Enhanced NLP for automated tagging.
*   Direct LLM-Airtable integration.
*   A custom web-based dashboard.
*   Prompt library management.
*   Support for multi-novel management.

This project was initiated by Patrick Somerville and developed with the assistance of the Manus AI agent.

