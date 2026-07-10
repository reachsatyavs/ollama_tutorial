#!/usr/bin/env python3
"""
AGENT 2: Markdown Documentation Generator

Generates markdown documentation files from prompts using Qwen.
Creates: FRD, Use Cases, Test Cases, Class Diagram

Usage:
    python 02_markdown_generator_agent.py \\
        --project "Event Registration Portal" \\
        --type frd \\
        --output-dir ./docs

Options:
    --project NAME        : Project name/description
    --type TYPE           : frd, usecases, testcases, classdiagram, all
    --output-dir DIR      : Directory to save markdown files (default: ./docs)
    --custom-prompt TEXT  : Custom prompt (overrides default)
"""

import requests
import argparse
import os
from pathlib import Path
from datetime import datetime


class MarkdownGeneratorAgent:
    """Generates markdown documentation using Qwen."""
    
    def __init__(self, ollama_url="http://localhost:11434", output_dir="./docs"):
        self.ollama_url = ollama_url
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.generated_files = []
    
    def call_qwen(self, prompt):
        """Call Qwen to generate content."""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "qwen2.5-coder:7b",
                    "prompt": prompt,
                    "temperature": 0.3,
                    "stream": True
                },
                timeout=300
            )
            return response.json()["response"]
        except Exception as e:
            print(f"❌ Error calling Qwen: {e}")
            return None
    
    def generate_frd(self, project_name):
        """Generate Functional Requirements Document."""
        print(f"\n📝 Generating FRD for: {project_name}")
        
        prompt = f"""Generate a professional Functional Requirements Document (FRD) for:
        
Project: {project_name}

Include sections:
1. Project Overview (1-2 paragraphs)
2. Objectives and Goals (bullet points)
3. User Types/Roles (who will use the system)
4. Core Features (main functionality)
5. Requirements:
   - Functional Requirements (what system does)
   - Non-Functional Requirements (performance, security, etc.)
6. Database Requirements (what data needs to be stored)

Use markdown format. Make it professional but concise."""
        
        return self.call_qwen(prompt)
    
    def generate_use_cases(self, project_name):
        """Generate Use Cases document."""
        print(f"\n📝 Generating Use Cases for: {project_name}")
        
        prompt = f"""Generate detailed Use Cases for:

Project: {project_name}

Create 4-6 use cases with format:
- Use Case Name
- Actor (who performs it)
- Precondition (what must be true first)
- Main Steps (numbered steps)
- Postcondition (what's true after)
- Alternative Flows (if any)

Use markdown format."""
        
        return self.call_qwen(prompt)
    
    def generate_test_cases(self, project_name):
        """Generate Test Cases document."""
        print(f"\n📝 Generating Test Cases for: {project_name}")
        
        prompt = f"""Generate comprehensive Test Cases for:

Project: {project_name}

Create 5-8 test cases with format:
- Test Case ID (TC-001, TC-002, etc.)
- Test Name
- Precondition
- Test Steps (numbered)
- Expected Result
- Status (Pass/Fail/Pending)

Include both positive and negative test cases.
Use markdown format."""
        
        return self.call_qwen(prompt)
    
    def generate_class_diagram(self, project_name):
        """Generate Class Diagram (as Mermaid or text description)."""
        print(f"\n📝 Generating Class Diagram for: {project_name}")
        
        prompt = f"""Generate a Class Diagram for:

Project: {project_name}

Use Mermaid diagram syntax (markdown compatible):

```mermaid
classDiagram
  class ClassName {{
    - property: type
    + method(): returnType
  }}
```

Include:
- Main classes/entities for the system
- Properties (with types)
- Methods
- Relationships (inheritance, association)

Make it realistic for the project.
Use markdown with Mermaid code block."""
        
        return self.call_qwen(prompt)
    
    def save_to_file(self, filename, content):
        """Save generated content to markdown file."""
        filepath = self.output_dir / filename
        
        try:
            with open(filepath, 'w') as f:
                f.write(content)
            
            print(f"   ✅ Saved: {filepath}")
            self.generated_files.append(filename)
            return True
        except Exception as e:
            print(f"   ❌ Failed to save {filepath}: {e}")
            return False
    
    def run(self, project_name, doc_types="all", custom_prompt=None):
        """Main execution."""
        print("\n" + "="*70)
        print(f"🚀 MARKDOWN DOCUMENTATION GENERATOR AGENT")
        print("="*70)
        print(f"Project: {project_name}\n")
        
        # Determine what to generate
        if doc_types == "all":
            types = ["frd", "usecases", "testcases", "classdiagram"]
        else:
            types = [doc_types]
        
        results = {}
        
        # Generate each type
        if "frd" in types:
            content = self.generate_frd(project_name)
            if content:
                results["frd"] = content
                self.save_to_file("01_FRD.md", content)
        
        if "usecases" in types:
            content = self.generate_use_cases(project_name)
            if content:
                results["usecases"] = content
                self.save_to_file("02_UseCases.md", content)
        
        if "testcases" in types:
            content = self.generate_test_cases(project_name)
            if content:
                results["testcases"] = content
                self.save_to_file("03_TestCases.md", content)
        
        if "classdiagram" in types:
            content = self.generate_class_diagram(project_name)
            if content:
                results["classdiagram"] = content
                self.save_to_file("04_ClassDiagram.md", content)
        
        # Summary
        print("\n" + "="*70)
        print(f"✅ Generated {len(self.generated_files)} files")
        print(f"📂 Saved to: {self.output_dir.absolute()}")
        print("="*70 + "\n")
        
        return len(self.generated_files) > 0


def main():
    parser = argparse.ArgumentParser(
        description="Generate markdown documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate FRD only
  python 02_markdown_generator_agent.py \\
    --project "Event Registration Portal" \\
    --type frd

  # Generate all documentation
  python 02_markdown_generator_agent.py \\
    --project "Event Registration Portal" \\
    --type all \\
    --output-dir ./project_docs

  # Generate specific type
  python 02_markdown_generator_agent.py \\
    --project "User Login System" \\
    --type testcases
        """
    )
    
    parser.add_argument('--project', type=str, required=True, help='Project name/description')
    parser.add_argument('--type', type=str, default='all', 
                       choices=['frd', 'usecases', 'testcases', 'classdiagram', 'all'],
                       help='Type of documentation to generate (default: all)')
    parser.add_argument('--output-dir', type=str, default='./docs', help='Output directory for markdown files')
    parser.add_argument('--custom-prompt', type=str, help='Custom prompt (overrides default)')
    
    args = parser.parse_args()
    
    # Create agent
    agent = MarkdownGeneratorAgent(output_dir=args.output_dir)
    
    # Run
    success = agent.run(
        project_name=args.project,
        doc_types=args.type,
        custom_prompt=args.custom_prompt
    )
    
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
