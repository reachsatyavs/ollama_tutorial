# 3 AI Agents: Usage Guide

**All agents connect to Ollama running locally on `http://localhost:11434`**

---

## **SETUP (Do This First)**

### **1. Make sure Ollama is running**
```bash
ollama serve
# In another terminal
```

### **2. Check model is available**
```bash
ollama list
# Should show: qwen2.5-coder:7b
```

### **3. Make scripts executable (optional)**
```bash
chmod +x 01_directory_creator_agent.py
chmod +x 02_markdown_generator_agent.py
chmod +x 03_code_generator_executor_agent.py
```

---

## **AGENT 1: Directory Structure Creator**

**Purpose:** Create project folder structure from JSON

### **Example 1A: From Existing JSON File**

```bash
# First, edit example_structure.json or create your own

python 01_directory_creator_agent.py \
  --json example_structure.json \
  --project my_event_portal
```

**Output:**
```
my_event_portal/
├── src/
│   ├── app.py
│   ├── models.py
│   ├── routes/
│   ├── utils.py
│   └── __init__.py
├── templates/
├── static/
├── tests/
├── config/
├── data/
└── logs/
```

### **Example 1B: Generate JSON from Qwen, Then Create**

```bash
python 01_directory_creator_agent.py \
  --generate-from-qwen \
  --prompt "Create directory structure for a Flask event registration system" \
  --project event_registration_portal
```

**What happens:**
1. Asks Qwen: "What directory structure do you recommend?"
2. Qwen generates JSON
3. Agent creates actual folders
4. Takes ~2-3 minutes (Qwen response time)

### **Example 1C: Minimal (Default)**

```bash
python 01_directory_creator_agent.py --project myapp
# Uses default structure
```

---

## **AGENT 2: Markdown Documentation Generator**

**Purpose:** Generate FRD, Use Cases, Test Cases, Class Diagrams

### **Example 2A: Generate All Documentation**

```bash
python 02_markdown_generator_agent.py \
  --project "Event Registration Portal" \
  --type all \
  --output-dir ./project_docs
```

**Creates:**
- `project_docs/01_FRD.md` (Functional Requirements)
- `project_docs/02_UseCases.md` (Use Cases)
- `project_docs/03_TestCases.md` (Test Cases)
- `project_docs/04_ClassDiagram.md` (Class Diagram)

### **Example 2B: Generate Specific Type**

```bash
# FRD only
python 02_markdown_generator_agent.py \
  --project "Event Registration Portal" \
  --type frd

# Use Cases only
python 02_markdown_generator_agent.py \
  --project "Event Registration Portal" \
  --type usecases

# Test Cases only
python 02_markdown_generator_agent.py \
  --project "Event Registration Portal" \
  --type testcases

# Class Diagram only
python 02_markdown_generator_agent.py \
  --project "Event Registration Portal" \
  --type classdiagram
```

### **Example 2C: Custom Project Description**

```bash
python 02_markdown_generator_agent.py \
  --project "User Login System with OAuth 2.0 and JWT tokens" \
  --type all \
  --output-dir ./login_system_docs
```

---

## **AGENT 3: Code Generator & Executor**

**Purpose:** Generate code and optionally run it

### **Example 3A: Generate Python Code**

```bash
python 03_code_generator_executor_agent.py \
  --prompt "Write a function to reverse a string" \
  --language python \
  --output reverse_string.py
```

**Output:**
```
Generated Code:
─────────────────────────────
def reverse_string(s):
    """Reverse a string."""
    return s[::-1]

if __name__ == "__main__":
    test_string = "Hello World"
    print(f"Original: {test_string}")
    print(f"Reversed: {reverse_string(test_string)}")
─────────────────────────────

✅ Code saved to: reverse_string.py

Run this code now? (y/n): y

🐍 Running Python code...
─────────────────────────────
Original: Hello World
Reversed: dlroW olleH
─────────────────────────────
```

### **Example 3B: Auto-Run (No Prompt)**

```bash
python 03_code_generator_executor_agent.py \
  --prompt "Calculate fibonacci numbers up to 20" \
  --language python \
  --output fib.py \
  --auto-run
```

### **Example 3C: Generate JavaScript**

```bash
python 03_code_generator_executor_agent.py \
  --prompt "Create a function to validate email addresses" \
  --language javascript \
  --output validate_email.js
```

### **Example 3D: Just Generate (Don't Run or Save)**

```bash
python 03_code_generator_executor_agent.py \
  --prompt "Write a quick sort algorithm" \
  --language python \
  --no-save \
  --auto-run
```

### **Example 3E: Generate with Input Data**

```bash
python 03_code_generator_executor_agent.py \
  --prompt "Read numbers from input and find the largest" \
  --language python \
  --output find_max.py \
  --input "5\n3\n8\n1"
```

---

## **WORKFLOW FOR YOUR SESSION**

### **Step 1: Generate Directory Structure**
```bash
python 01_directory_creator_agent.py \
  --generate-from-qwen \
  --prompt "Create directory structure for Flask event registration portal" \
  --project event_portal

# Takes ~2-3 minutes
```

### **Step 2: Generate Documentation**
```bash
python 02_markdown_generator_agent.py \
  --project "Event Registration Portal" \
  --type all \
  --output-dir ./event_portal/docs

# Takes ~2-3 minutes per document
```

### **Step 3: Generate Code**
```bash
# Generate login function
python 03_code_generator_executor_agent.py \
  --prompt "Write a login function that checks email and password against a database" \
  --language python \
  --output event_portal/src/login.py

# Takes ~2-3 minutes
```

---

## **SECURITY NOTES**

### **Blocked Operations**
```
❌ os.remove()           - Can't delete files
❌ os.rmdir()            - Can't delete directories
❌ shutil.rmtree()       - Can't delete folder trees
❌ os.system()           - Can't run system commands
❌ subprocess.Popen()    - Can't run processes
❌ eval()                - Can't execute strings as code
❌ exec()                - Can't execute strings as code
```

### **Example: Blocked Code**
```python
# This will be blocked:
os.remove("important_file.txt")  # ❌ Blocked
```

### **Always Review Generated Code**
Before running:
1. Check for suspicious imports
2. Verify file operations
3. Look for network calls
4. Run in isolated environment first

---

## **TIPS & TRICKS**

### **Tip 1: Better Prompts = Better Code**
```
Bad prompt: "Write a login function"

Good prompt: "Write a Python function that:
- Takes email and password as parameters
- Validates email format using regex
- Checks password length (min 8 chars)
- Returns True if valid, False otherwise
- Includes docstring with examples"
```

### **Tip 2: Multiple Calls**
```bash
# First call: Generate structure
python 01_directory_creator_agent.py ...

# Second call: Generate docs
python 02_markdown_generator_agent.py ...

# Third call: Generate code
python 03_code_generator_executor_agent.py ...

# Each can take 2-3 minutes, so total: ~10 minutes
```

### **Tip 3: Reuse Generated Output**
```bash
# Generate once
python 02_markdown_generator_agent.py --project "My App" --type frd

# View multiple times
cat docs/01_FRD.md
cat docs/01_FRD.md  # No need to regenerate
```

### **Tip 4: Customize Output Directory**
```bash
# All docs in one place
python 02_markdown_generator_agent.py \
  --project "MyApp" \
  --type all \
  --output-dir ./documentation

# vs

# In project folder
python 02_markdown_generator_agent.py \
  --project "MyApp" \
  --type all \
  --output-dir ./myapp/docs
```

---

## **TROUBLESHOOTING**

### **Problem: "Cannot connect to Ollama"**
```bash
# Solution: Make sure Ollama is running
ollama serve

# In another terminal, test
curl http://localhost:11434/api/tags
```

### **Problem: "Model not found"**
```bash
# Check installed models
ollama list

# If qwen2.5-coder:7b not there, download it
ollama pull qwen2.5-coder:7b

# Takes ~5-10 minutes depending on internet
```

### **Problem: "Code execution timeout"**
```bash
# Code took too long to run
# Default timeout: 30 seconds

# Either:
# 1. Wait for Qwen to finish
# 2. Cancel and try simpler prompt
# 3. Check if code has infinite loop
```

### **Problem: "Node.js not found"**
```bash
# You need Node.js installed to run JavaScript

# Install from: https://nodejs.org/
# Then test: node --version
```

---

## **EXAMPLE SESSION FLOW (90 minutes)**

```
0-15 min:   Explain AI, SLM, Ollama, security
15-20 min:  Run Agent 1 (Directory) → Shows folder creation
20-25 min:  Run Agent 2 (Markdown) → Shows FRD generation
25-30 min:  Run Agent 3 (Code) → Shows login program
30-60 min:  Students run agents for their own projects
60-90 min:  Q&A, review outputs, discuss next steps
```

---

## **QUICK REFERENCE**

```bash
# Agent 1: Directories
python 01_directory_creator_agent.py --json structure.json --project myapp

# Agent 2: Documentation
python 02_markdown_generator_agent.py --project "My App" --type all

# Agent 3: Code
python 03_code_generator_executor_agent.py --prompt "..." --output file.py --auto-run
```

---

**That's it! You're ready to use the agents.**
