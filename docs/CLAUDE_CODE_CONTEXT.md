# Claude Code Context: AI Agents System

**Use this document in Claude Code (VS Code) for further enhancements**

---

## **System Overview**

You have 3 AI agents that connect to Ollama (localhost:11434):

### **Agent 1: Directory Creator** (`01_directory_creator_agent.py`)
- **Input:** JSON file or Qwen prompt
- **Output:** Actual folder structure on disk
- **Language:** Python
- **Time:** 2-5 seconds (JSON file) or 2-3 minutes (Qwen generation)

### **Agent 2: Markdown Generator** (`02_markdown_generator_agent.py`)
- **Input:** Project name + document type
- **Output:** Markdown files (FRD, Use Cases, Test Cases, Class Diagram)
- **Language:** Python
- **Time:** 2-3 minutes per document

### **Agent 3: Code Generator & Executor** (`03_code_generator_executor_agent.py`)
- **Input:** Prompt + language (Python/JavaScript)
- **Output:** Generated code + optional execution
- **Language:** Python
- **Time:** 2-3 minutes to generate

---

## **Ollama Connection Details**

All agents connect via:
```python
requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "qwen2.5-coder:7b",
        "prompt": prompt,
        "temperature": 0.2-0.3,
        "stream": False
    }
)
```

---

## **What Claude Code Can Help With**

### **Enhancements You Might Want**

1. **Add progress bar** (show generation progress)
2. **Parallel execution** (run agents simultaneously)
3. **Template library** (pre-built JSON structures)
4. **Web UI** (Flask app to run agents via browser)
5. **Config file** (customize Ollama URL, model, temp)
6. **Logging** (save all outputs to log files)
7. **Batch mode** (run multiple agents in sequence)
8. **Error recovery** (retry on failure)
9. **Environment variables** (OLLAMA_URL, MODEL_NAME)
10. **Docker support** (containerize the system)

---

## **Example Improvements You Can Ask Claude Code**

### **Example 1: Add Progress Display**
```
"Add a progress bar to show generation status. 
 Use tokens generated vs total expected."
```

### **Example 2: Auto-Retry on Timeout**
```
"If Ollama times out, automatically retry up to 3 times 
 with exponential backoff."
```

### **Example 3: Config File Support**
```
"Create a config.yaml file that agents can read for:
- Ollama URL
- Model name
- Temperature
- Output directory
- Timeout value"
```

### **Example 4: Batch Processing**
```
"Create a batch_run.py that can execute multiple agents 
 in sequence with one command:
 - Generate structure
 - Generate docs
 - Generate code
 All from one config file."
```

### **Example 5: Web UI**
```
"Create a simple Flask web app with:
- Form for directory structure input
- Form for documentation prompts
- Form for code generation
- Display results in browser"
```

### **Example 6: Template Library**
```
"Create pre-built JSON templates for common projects:
- Flask web app
- Node.js REST API
- Django project
- FastAPI application
Users can select template instead of writing JSON."
```

---

## **How to Use Claude Code**

### **In VS Code:**

1. **Select the agent file** you want to enhance
2. **Open Claude Code** (bottom-right)
3. **Ask Claude** to make improvements

**Examples:**

```
"Add logging to 01_directory_creator_agent.py. 
 Log all created directories to a file with timestamps."
```

```
"Enhance 02_markdown_generator_agent.py to support 
 custom prompts for each document type."
```

```
"Modify 03_code_generator_executor_agent.py to show 
 code formatting issues using pylint for Python."
```

---

## **Agent Class Structure**

### **Agent 1: DirectoryCreatorAgent**
```python
class DirectoryCreatorAgent:
    def generate_structure_from_qwen(prompt)  # Ask Qwen
    def load_structure_from_json(filepath)    # Read file
    def parse_json_string(json_str)           # Extract JSON
    def create_directories(structure)         # Create folders
    def create_init_files()                   # Add __init__.py
    def run()                                 # Main execution
```

### **Agent 2: MarkdownGeneratorAgent**
```python
class MarkdownGeneratorAgent:
    def call_qwen(prompt)           # Call Qwen
    def generate_frd(project_name)  # Generate FRD
    def generate_use_cases()        # Generate use cases
    def generate_test_cases()       # Generate test cases
    def generate_class_diagram()    # Generate diagram
    def save_to_file(filename, content)  # Save markdown
    def run()                       # Main execution
```

### **Agent 3: CodeGeneratorExecutorAgent**
```python
class CodeGeneratorExecutorAgent:
    def call_qwen(prompt)           # Ask Qwen
    def extract_code_block(response)  # Parse response
    def check_security(code)        # Check for blocked ops
    def save_code(filepath, code)   # Save to file
    def run_python(filepath)        # Execute Python
    def run_javascript(filepath)    # Execute Node.js
    def run()                       # Main execution
```

---

## **Security Implementation**

### **Blocked Operations** (Agent 3)
```python
BLOCKED_KEYWORDS = [
    "os.remove", "os.rmdir", "os.unlink",
    "shutil.rmtree", "shutil.remove",
    "subprocess.call", "subprocess.Popen",
    "os.system", "os.popen",
    "eval(", "exec("
]
```

**Add more restrictions by:**
1. Adding keywords to BLOCKED_KEYWORDS list
2. Creating a separate `security_rules.yaml` file
3. Sandboxing code execution (Docker)

---

## **Command-Line Interface**

### **Agent 1 Arguments**
```
--json FILE              : JSON file with structure
--project NAME           : Project name
--generate-from-qwen     : Generate from Qwen
--prompt TEXT            : Prompt for Qwen
```

### **Agent 2 Arguments**
```
--project NAME           : Project name
--type [frd|usecases|testcases|classdiagram|all]
--output-dir DIR         : Where to save files
--custom-prompt TEXT     : Override default prompt
```

### **Agent 3 Arguments**
```
--prompt TEXT            : Code to generate
--language [python|javascript]
--output FILE            : Save to file
--auto-run               : Don't ask, just run
--no-save                : Don't save to file
--input DATA             : Input for running code
```

---

## **Files Included**

```
01_directory_creator_agent.py       (~150 lines)
02_markdown_generator_agent.py       (~180 lines)
03_code_generator_executor_agent.py  (~250 lines)
example_structure.json               (example JSON)
AGENTS_USAGE_GUIDE.md               (this file)
CLAUDE_CODE_CONTEXT.md              (reference)
```

---

## **Common Enhancement Patterns**

### **Pattern 1: Add Retry Logic**
```python
def call_qwen_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            # call qwen
            return response
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # exponential backoff
            else:
                raise
```

### **Pattern 2: Add Logging**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agents.log'),
        logging.StreamHandler()
    ]
)

logging.info("Starting agent...")
```

### **Pattern 3: Add Config File Support**
```python
import yaml

config = yaml.safe_load(open('config.yaml'))
OLLAMA_URL = config.get('ollama_url', 'http://localhost:11434')
MODEL = config.get('model', 'qwen2.5-coder:7b')
TIMEOUT = config.get('timeout', 300)
```

### **Pattern 4: Add Progress Tracking**
```python
from tqdm import tqdm

for item in tqdm(items, desc="Processing"):
    # do work
    pass
```

---

## **Testing Each Agent**

### **Test Agent 1**
```bash
# Create test directory
mkdir test_project
cd test_project

# Run with example JSON
python ../01_directory_creator_agent.py \
    --json ../example_structure.json \
    --project test_app

# Verify structure
tree test_app
```

### **Test Agent 2**
```bash
python ../02_markdown_generator_agent.py \
    --project "Test Project" \
    --type frd \
    --output-dir ./docs

# Verify output
cat docs/01_FRD.md
```

### **Test Agent 3**
```bash
python ../03_code_generator_executor_agent.py \
    --prompt "Print hello world" \
    --language python \
    --output test.py \
    --auto-run
```

---

## **Integration Ideas**

### **Idea 1: Combine All Three**
```bash
# One command to:
# 1. Create directory structure
# 2. Generate documentation
# 3. Generate starter code

python master_agent.py --project "MyApp"
```

### **Idea 2: Web Dashboard**
```python
# Flask app showing:
# - Agent status
# - Generated files
# - Execution history
# - Download results
```

### **Idea 3: IDE Integration**
```python
# VS Code extension that:
# - Right-click → Generate structure
# - Right-click → Generate docs
# - Right-click → Generate code
```

### **Idea 4: Git Integration**
```python
# Auto-commit generated files to git
# Generate with: git add, commit message, etc.
```

---

## **Next Steps for Enhancement**

**Priority 1 (Easy, High Value):**
- [ ] Add logging to all agents
- [ ] Add config file support
- [ ] Better error messages

**Priority 2 (Medium, High Value):**
- [ ] Retry logic with backoff
- [ ] Progress bars
- [ ] Template library

**Priority 3 (Complex, Nice to Have):**
- [ ] Web UI
- [ ] Batch processing
- [ ] Docker containerization
- [ ] IDE plugin

---

## **Ask Claude Code For:**

**Syntax questions:** "How do I parse YAML in Python?"

**Feature requests:** "Add retry logic with exponential backoff"

**Bug fixes:** "Agent times out when generating large files"

**Refactoring:** "Make the code more DRY (Don't Repeat Yourself)"

**Performance:** "Optimize Agent 2 to generate docs faster"

**Testing:** "Write unit tests for Agent 1"

---

**Use this document as reference when working with Claude Code to enhance your agents!**
