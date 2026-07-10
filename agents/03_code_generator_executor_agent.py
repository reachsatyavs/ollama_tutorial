#!/usr/bin/env python3
"""
AGENT 3: Code Generator and Executor

Generates code from prompts and optionally executes it.
Supports Python and Node.js.

Usage:
    python 03_code_generator_executor_agent.py \\
        --prompt "Write a function to reverse a string" \\
        --language python \\
        --output reverse_string.py

Options:
    --prompt TEXT        : What code to generate (required)
    --language LANG      : python or javascript (default: python)
    --output FILE        : Where to save the code (required)
    --auto-run           : Run code without asking
    --no-save            : Don't save to file
    --input DATA         : Input for running code (optional)

Security Features:
    - Blocks: os.remove, os.system, shutil.rmtree, subprocess.call
    - Blocks: eval, exec for untrusted code
    - Examples provided in help
"""

import requests
import argparse
import os
import subprocess
import sys
from pathlib import Path


class CodeGeneratorExecutorAgent:
    """Generates and executes code using Qwen."""
    
    BLOCKED_KEYWORDS = [
        "os.remove", "os.rmdir", "os.unlink",
        "shutil.rmtree", "shutil.remove",
        "subprocess.call", "subprocess.Popen",
        "os.system", "os.popen",
        "eval(", "exec(",
        "glob.glob", "__import__",
    ]
    
    def __init__(self, ollama_url="http://localhost:11434"):
        self.ollama_url = ollama_url
        self.language = None
        self.code = None
    
    def call_qwen(self, prompt):
        """Call Qwen to generate code."""
        print(f"\n🔄 Asking Qwen to generate code...")
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "qwen2.5-coder:7b",
                    "prompt": prompt,
                    "temperature": 0.2,
                    "stream": False
                },
                timeout=300
            )
            
            code = response.json()["response"]
            print(f"✅ Code generated successfully\n")
            return code
        except Exception as e:
            print(f"❌ Error calling Qwen: {e}")
            return None
    
    def extract_code_block(self, response):
        """Extract code from markdown code blocks if present."""
        # Look for ```python ... ``` or ```javascript ... ```
        import re
        
        # Try to find code blocks
        for pattern in [r'```(?:python|py)(.*?)```', r'```(?:javascript|js|node)(.*?)```', r'```(.*?)```']:
            match = re.search(pattern, response, re.DOTALL)
            if match:
                return match.group(1).strip()
        
        # If no code blocks, return as-is
        return response.strip()
    
    def check_security(self, code):
        """Check for dangerous operations."""
        for keyword in self.BLOCKED_KEYWORDS:
            if keyword in code:
                print(f"⚠️  WARNING: Found potentially dangerous operation: {keyword}")
                print(f"   This operation is blocked for security reasons.")
                return False
        
        return True
    
    def save_code(self, filepath, code):
        """Save code to file."""
        try:
            with open(filepath, 'w') as f:
                f.write(code)
            
            print(f"✅ Code saved to: {filepath}\n")
            return True
        except Exception as e:
            print(f"❌ Error saving file: {e}")
            return False
    
    def run_python(self, filepath, input_data=None):
        """Execute Python code."""
        print(f"🐍 Running Python code...\n")
        print("="*70)
        
        try:
            if input_data:
                result = subprocess.run(
                    ["python", filepath],
                    input=input_data,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            else:
                result = subprocess.run(
                    ["python", filepath],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            
            print(result.stdout)
            
            if result.stderr:
                print(f"Errors:\n{result.stderr}")
            
            print("="*70 + "\n")
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            print("❌ Code execution timed out (>30 seconds)")
            return False
        except Exception as e:
            print(f"❌ Error executing Python: {e}")
            return False
    
    def run_javascript(self, filepath, input_data=None):
        """Execute JavaScript code."""
        print(f"📜 Running JavaScript code...\n")
        print("="*70)
        
        try:
            # Try node first
            result = subprocess.run(
                ["node", filepath],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            print(result.stdout)
            
            if result.stderr:
                print(f"Errors:\n{result.stderr}")
            
            print("="*70 + "\n")
            return result.returncode == 0
        except FileNotFoundError:
            print("❌ Node.js not found. Install Node.js to run JavaScript.")
            return False
        except subprocess.TimeoutExpired:
            print("❌ Code execution timed out (>30 seconds)")
            return False
        except Exception as e:
            print(f"❌ Error executing JavaScript: {e}")
            return False
    
    def run(self, prompt, language="python", output_file=None, auto_run=False, no_save=False, input_data=None):
        """Main execution."""
        print("\n" + "="*70)
        print(f"🚀 CODE GENERATOR & EXECUTOR AGENT")
        print("="*70)
        print(f"Language: {language.upper()}")
        print(f"Prompt: {prompt}\n")
        
        # Validate
        if language.lower() not in ["python", "javascript", "js", "node"]:
            print(f"❌ Unsupported language: {language}")
            return False
        
        self.language = language.lower()
        
        if not output_file and not no_save:
            print("❌ --output is required (unless using --no-save)")
            return False
        
        # Format prompt
        lang_name = "Python" if self.language == "python" else "JavaScript"
        format_prompt = f"""Generate a complete {lang_name} program for:

{prompt}

Requirements:
- Include all imports
- Make it runnable (not just snippets)
- Add comments explaining key parts
- Handle errors gracefully
- If it takes input, use input() or readline

Return ONLY the code, no explanations."""
        
        # Generate
        raw_code = self.call_qwen(format_prompt)
        if not raw_code:
            return False
        
        # Extract code from markdown if present
        self.code = self.extract_code_block(raw_code)
        
        # Security check
        if not self.check_security(self.code):
            print("❌ Code blocked for security reasons")
            return False
        
        # Show generated code
        print(f"Generated Code:\n")
        print("-"*70)
        print(self.code)
        print("-"*70 + "\n")
        
        # Save if requested
        if not no_save and output_file:
            if not self.save_code(output_file, self.code):
                return False
        
        # Ask to run
        if auto_run:
            run_now = "y"
        else:
            run_now = input("Run this code now? (y/n): ").lower().strip()
        
        if run_now == "y":
            if self.language == "python":
                return self.run_python(output_file or "temp_code.py", input_data)
            else:
                return self.run_javascript(output_file or "temp_code.js", input_data)
        else:
            print("✅ Code saved. You can run it later.")
            return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate and execute code using Qwen",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate and save Python code
  python 03_code_generator_executor_agent.py \\
    --prompt "Write a function to reverse a string" \\
    --language python \\
    --output reverse.py

  # Generate and auto-run
  python 03_code_generator_executor_agent.py \\
    --prompt "Calculate fibonacci numbers up to 20" \\
    --language python \\
    --output fib.py \\
    --auto-run

  # Generate JavaScript
  python 03_code_generator_executor_agent.py \\
    --prompt "Create a function to validate email" \\
    --language javascript \\
    --output validate.js

  # Generate without saving (just execute)
  python 03_code_generator_executor_agent.py \\
    --prompt "Print 'Hello World'" \\
    --language python \\
    --no-save \\
    --auto-run

Security:
  Blocked operations: os.remove, os.system, exec, eval, shutil.rmtree
  Use --no-save if you don't trust the generated code
  Always review generated code before running
        """
    )
    
    parser.add_argument('--prompt', type=str, required=True, help='What code to generate')
    parser.add_argument('--language', type=str, default='python', 
                       choices=['python', 'javascript', 'js', 'node'],
                       help='Programming language (default: python)')
    parser.add_argument('--output', type=str, help='File to save code to')
    parser.add_argument('--auto-run', action='store_true', help='Run without asking')
    parser.add_argument('--no-save', action='store_true', help='Don\'t save to file')
    parser.add_argument('--input', type=str, help='Input data for running code')
    
    args = parser.parse_args()
    
    # Validate
    if not args.output and not args.no_save:
        print("Error: Either --output or --no-save is required")
        parser.print_help()
        exit(1)
    
    # Create agent
    agent = CodeGeneratorExecutorAgent()
    
    # Run
    success = agent.run(
        prompt=args.prompt,
        language=args.language,
        output_file=args.output,
        auto_run=args.auto_run,
        no_save=args.no_save,
        input_data=args.input
    )
    
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
