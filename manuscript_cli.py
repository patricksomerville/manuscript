#!/usr/bin/env python3
"""
Manuscript Workflow CLI
A unified command-line interface for managing novel generation workflows.
"""

import argparse
import sys
import os
import json
from pathlib import Path

# Import existing scripts (optional - only when needed)
try:
    import segmenter_script
except ImportError:
    segmenter_script = None

try:
    import airtable_uploader
except ImportError:
    airtable_uploader = None

try:
    import fetch_airtable_data
except ImportError:
    fetch_airtable_data = None

try:
    import chapter_assembler
except ImportError:
    chapter_assembler = None

try:
    import generate_analytics_script
except ImportError:
    generate_analytics_script = None


class ManuscriptCLI:
    """Main CLI controller for manuscript workflow."""
    
    def __init__(self):
        self.config_file = Path.home() / ".manuscript" / "config.json"
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file or return defaults."""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {
            "airtable_api_key": os.getenv("AIRTABLE_API_KEY", ""),
            "airtable_base_id": os.getenv("AIRTABLE_BASE_ID", ""),
            "default_output_dir": str(Path.cwd() / "output"),
            "known_characters": []
        }
    
    def save_config(self):
        """Save configuration to file."""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
        print(f"✓ Configuration saved to {self.config_file}")
    
    def cmd_init(self, args):
        """Initialize manuscript project configuration."""
        print("📚 Manuscript Workflow Initialization")
        print("=" * 50)
        
        if args.airtable_key:
            self.config["airtable_api_key"] = args.airtable_key
        if args.airtable_base:
            self.config["airtable_base_id"] = args.airtable_base
        if args.output_dir:
            self.config["default_output_dir"] = args.output_dir
        
        self.save_config()
        
        # Create output directory
        output_dir = Path(self.config["default_output_dir"])
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n✓ Project initialized")
        print(f"  Output directory: {output_dir}")
        print(f"  Config file: {self.config_file}")
    
    def cmd_segment(self, args):
        """Segment a chapter into text segments."""
        print(f"📄 Segmenting chapter {args.chapter_id}...")
        
        input_file = Path(args.input)
        if not input_file.exists():
            print(f"❌ Error: Input file not found: {input_file}")
            return 1
        
        output_file = Path(args.output) if args.output else \
                     Path(self.config["default_output_dir"]) / f"{args.chapter_id}_segments.json"
        
        # Call segmenter
        with open(input_file, 'r', encoding='utf-8') as f:
            chapter_content = f.read()
        
        segmented_data = segmenter_script.segment_chapter(chapter_content, args.chapter_id)
        
        chapter_output = {
            "ChapterID": args.chapter_id,
            "Segments": segmented_data
        }
        
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(chapter_output, f, indent=4, ensure_ascii=False)
        
        print(f"✓ Segmented {len(segmented_data)} segments")
        print(f"✓ Saved to {output_file}")
        return 0
    
    def cmd_upload(self, args):
        """Upload segments to Airtable."""
        print(f"☁️  Uploading to Airtable...")
        
        if not self.config.get("airtable_api_key") or not self.config.get("airtable_base_id"):
            print("❌ Error: Airtable credentials not configured.")
            print("   Run: manuscript init --airtable-key YOUR_KEY --airtable-base YOUR_BASE")
            return 1
        
        # Set environment variables for airtable_uploader
        os.environ["AIRTABLE_API_KEY"] = self.config["airtable_api_key"]
        os.environ["AIRTABLE_BASE_ID"] = self.config["airtable_base_id"]
        
        input_file = Path(args.input)
        if not input_file.exists():
            print(f"❌ Error: Input file not found: {input_file}")
            return 1
        
        print(f"✓ Uploading from {input_file}")
        # Note: airtable_uploader would need to be refactored to be callable as a function
        print("⚠️  Upload functionality requires airtable_uploader.py to be refactored")
        return 0
    
    def cmd_fetch(self, args):
        """Fetch data from Airtable."""
        print(f"⬇️  Fetching from Airtable...")
        
        if not self.config.get("airtable_api_key") or not self.config.get("airtable_base_id"):
            print("❌ Error: Airtable credentials not configured.")
            return 1
        
        os.environ["AIRTABLE_API_KEY"] = self.config["airtable_api_key"]
        os.environ["AIRTABLE_BASE_ID"] = self.config["airtable_base_id"]
        
        output_dir = Path(args.output) if args.output else Path(self.config["default_output_dir"])
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"✓ Fetching to {output_dir}")
        print("⚠️  Fetch functionality requires fetch_airtable_data.py to be refactored")
        return 0
    
    def cmd_assemble(self, args):
        """Assemble chapter from segments."""
        print(f"📖 Assembling chapter {args.chapter_id}...")
        
        # This would call chapter_assembler functionality
        print("⚠️  Assemble functionality requires chapter_assembler.py to be refactored")
        return 0
    
    def cmd_analytics(self, args):
        """Generate analytics from Airtable data."""
        print(f"📊 Generating analytics...")
        
        # This would call generate_analytics_script functionality
        print("⚠️  Analytics functionality requires generate_analytics_script.py to be refactored")
        return 0
    
    def cmd_status(self, args):
        """Show project status."""
        print("📚 Manuscript Workflow Status")
        print("=" * 50)
        print(f"Config file: {self.config_file}")
        print(f"Config exists: {'✓' if self.config_file.exists() else '❌'}")
        print(f"\nAirtable configured: {'✓' if self.config.get('airtable_api_key') else '❌'}")
        print(f"Output directory: {self.config.get('default_output_dir', 'Not set')}")
        
        output_dir = Path(self.config.get("default_output_dir", "."))
        if output_dir.exists():
            json_files = list(output_dir.glob("*.json"))
            print(f"\nOutput files: {len(json_files)}")
            for f in json_files[:5]:
                print(f"  - {f.name}")
            if len(json_files) > 5:
                print(f"  ... and {len(json_files) - 5} more")
        return 0


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="Manuscript Workflow - Novel generation and management system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Initialize project
  manuscript init --airtable-key YOUR_KEY --airtable-base YOUR_BASE
  
  # Segment a chapter
  manuscript segment chapter01.txt CH001
  
  # Check project status
  manuscript status
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Init command
    init_parser = subparsers.add_parser('init', help='Initialize manuscript project')
    init_parser.add_argument('--airtable-key', help='Airtable API key')
    init_parser.add_argument('--airtable-base', help='Airtable base ID')
    init_parser.add_argument('--output-dir', help='Default output directory')
    
    # Segment command
    segment_parser = subparsers.add_parser('segment', help='Segment a chapter')
    segment_parser.add_argument('input', help='Input chapter file')
    segment_parser.add_argument('chapter_id', help='Chapter ID (e.g., CH001)')
    segment_parser.add_argument('-o', '--output', help='Output JSON file')
    
    # Upload command
    upload_parser = subparsers.add_parser('upload', help='Upload segments to Airtable')
    upload_parser.add_argument('input', help='Input JSON file with segments')
    
    # Fetch command
    fetch_parser = subparsers.add_parser('fetch', help='Fetch data from Airtable')
    fetch_parser.add_argument('-o', '--output', help='Output directory')
    
    # Assemble command
    assemble_parser = subparsers.add_parser('assemble', help='Assemble chapter from segments')
    assemble_parser.add_argument('chapter_id', help='Chapter ID to assemble')
    assemble_parser.add_argument('-o', '--output', help='Output file')
    
    # Analytics command
    analytics_parser = subparsers.add_parser('analytics', help='Generate analytics')
    analytics_parser.add_argument('-o', '--output', help='Output file')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show project status')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    cli = ManuscriptCLI()
    
    # Route to appropriate command
    command_map = {
        'init': cli.cmd_init,
        'segment': cli.cmd_segment,
        'upload': cli.cmd_upload,
        'fetch': cli.cmd_fetch,
        'assemble': cli.cmd_assemble,
        'analytics': cli.cmd_analytics,
        'status': cli.cmd_status,
    }
    
    return command_map[args.command](args)


if __name__ == "__main__":
    sys.exit(main())

