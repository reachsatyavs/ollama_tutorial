#!/usr/bin/env python3
"""
AGENT 1: Directory Structure Creator

Takes a JSON file describing directory structure and creates actual folders.
JSON can come from Qwen model or be manually created.

Usage:
    python 01_directory_creator_agent.py --json config.json --project myproject

Options:
    --json FILE          : Path to JSON file with directory structure
    --project NAME       : Root project name (optional, default: "project")
    --generate-from-qwen : Generate JSON from Qwen first (requires --prompt)
    --prompt PROMPT      : Prompt to send to Qwen for generating structure
"""

import json
import os
import argparse
import requests
from pathlib import Path


class DirectoryCreatorAgent:
    """Creates directory structure from JSON input."""
    
    def __init__(self, project_name="project", ollama_url="http://localhost:11434"):
        self.project_name = project_name
        self.ollama_url = ollama_url
        self.project_path = Path(project_name)
        self.created_dirs = []
    
    def generate_structure_from_qwen(self, prompt):
        """
        Ask Qwen to generate directory structure as JSON.
        """
        print(f"\n📝 Asking Qwen to generate directory structure...")
        print(f"   Prompt: {prompt}\n")
        
        # Add instruction to return JSON
        full_prompt = f"""{prompt}

Return ONLY a valid JSON object representing the directory structure.
Use nested objects where folders contain subfolders.

Example format:
{{
  "src": {{}},
  "templates": {{}},
  "static": {{
    "css": {{}},
    "js": {{}}
  }},
  "tests": {{}},
  "config": {{}},
  "data": {{}}
}}

Return ONLY the JSON, no explanations."""
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "qwen2.5-coder:7b",
                    "prompt": full_prompt,
                    "temperature": 0.2,
                    "stream": False
                },
                timeout=300
            )
            
            output = response.json()["response"]
            print(f"✅ Qwen generated structure:\n{output}\n")
            return output
            
        except Exception as e:
            print(f"❌ Error calling Qwen: {e}")
            return None
    
    def load_structure_from_json(self, json_file):
        """Load directory structure from JSON file."""
        try:
            with open(json_file, 'r') as f:
                structure = json.load(f)
            print(f"✅ Loaded structure from: {json_file}")
            return structure
        except FileNotFoundError:
            print(f"❌ JSON file not found: {json_file}")
            return None
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON in file: {json_file}")
            return None
    
    def parse_json_string(self, json_str):
        """Parse JSON string into structure."""
        try:
            # Try to extract JSON from Qwen's response
            # Qwen might include some text before/after JSON
            json_start = json_str.find('{')
            json_end = json_str.rfind('}') + 1
            
            if json_start == -1:
                print("❌ No valid JSON found in response")
                return None
            
            json_clean = json_str[json_start:json_end]
            structure = json.loads(json_clean)
            return structure
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON: {e}")
            return None
    
    def create_directories(self, structure, current_path=None):
        """Recursively create directories from structure."""
        if current_path is None:
            current_path = self.project_path
        
        if not isinstance(structure, dict):
            return
        
        for folder_name, subfolders in structure.items():
            folder_path = current_path / folder_name
            
            try:
                folder_path.mkdir(parents=True, exist_ok=True)
                self.created_dirs.append(str(folder_path))
                print(f"   ✓ Created: {folder_path}")
            except Exception as e:
                print(f"   ✗ Failed to create {folder_path}: {e}")
                continue
            
            # Recursively create subfolders
            if isinstance(subfolders, dict) and subfolders:
                self.create_directories(subfolders, folder_path)
    
    def create_init_files(self):
        """Create __init__.py files in Python directories."""
        init_dirs = ["src", "tests", "config"]
        
        for init_dir in init_dirs:
            init_path = self.project_path / init_dir / "__init__.py"
            if init_path.parent.exists():
                init_path.touch()
                print(f"   ✓ Created: {init_path}")
    
    def run(self, json_input=None, generate_from_qwen=False, qwen_prompt=None):
        """Main execution."""
        print("\n" + "="*70)
        print(f"🚀 DIRECTORY STRUCTURE CREATOR AGENT")
        print("="*70)
        print(f"Project: {self.project_name}\n")
        
        # Get structure
        if generate_from_qwen and qwen_prompt:
            qwen_output = self.generate_structure_from_qwen(qwen_prompt)
            if not qwen_output:
                print("❌ Failed to generate from Qwen")
                return False
            
            structure = self.parse_json_string(qwen_output)
            if not structure:
                return False
        
        elif json_input:
            structure = self.load_structure_from_json(json_input)
            if not structure:
                return False
        
        else:
            print("❌ Must provide either --json or --generate-from-qwen")
            return False
        
        # Create directories
        print(f"\n📁 Creating directory structure...\n")
        self.create_directories(structure)
        
        # Create __init__.py files
        print(f"\n📄 Creating Python init files...\n")
        self.create_init_files()
        
        # Summary
        print("\n" + "="*70)
        print(f"✅ SUCCESS! Created {len(self.created_dirs)} directories")
        print(f"📂 Project location: {self.project_path.absolute()}")
        print("="*70 + "\n")
        
        return True


def main():
    parser = argparse.ArgumentParser(
        description="Create directory structure from JSON",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # From existing JSON file
  python 01_directory_creator_agent.py --json structure.json --project myapp

  # Generate from Qwen then create
  python 01_directory_creator_agent.py \\
    --generate-from-qwen \\
    --prompt "Create directory structure for event registration portal" \\
    --project event_portal

  # Minimal (uses default structure)
  python 01_directory_creator_agent.py --project myproject
        """
    )
    
    parser.add_argument('--json', type=str, help='Path to JSON file with directory structure')
    parser.add_argument('--project', type=str, default='project', help='Project name (default: project)')
    parser.add_argument('--generate-from-qwen', action='store_true', help='Generate structure from Qwen')
    parser.add_argument('--prompt', type=str, help='Prompt for Qwen to generate structure')
    
    args = parser.parse_args()
    
    # Create agent
    agent = DirectoryCreatorAgent(project_name=args.project)
    
    # Run
    success = agent.run(
        json_input=args.json,
        generate_from_qwen=args.generate_from_qwen,
        qwen_prompt=args.prompt
    )
    
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
