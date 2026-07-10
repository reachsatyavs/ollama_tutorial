# Quick Start: Test Your Agents (5 minutes)

**Test everything before your session**

---

## **Step 1: Verify Ollama is Running (30 seconds)**

```bash
# Terminal 1: Start Ollama
ollama serve

# You should see:
# [GIN-debug] Loaded binaries at /Users/.../bin
# [INFO] Starting ollama
```

---

## **Step 2: Verify Model is Available (30 seconds)**

```bash
# Terminal 2 (new terminal)
ollama list

# Should show:
# qwen2.5-coder:7b     13B    2.6GB    2 hours ago
```

If NOT present:
```bash
ollama pull qwen2.5-coder:7b
# Takes 5-10 minutes
```

---

## **Step 3: Test Agent 1 (2 minutes)**

```bash
# Make sure you're in the directory with the agents

python 01_directory_creator_agent.py \
  --json example_structure.json \
  --project test_event_portal

# Expected output:
# 🚀 DIRECTORY STRUCTURE CREATOR AGENT
# ========================================
# Project: test_event_portal
# ✅ Loaded structure from: example_structure.json
# 📁 Creating directory structure...
#    ✓ Created: test_event_portal/src
#    ✓ Created: test_event_portal/templates
#    ✓ Created: test_event_portal/static/css
#    ✓ Created: test_event_portal/static/js
#    [more folders...]
# ✅ SUCCESS! Created 15 directories
```

**Verify:**
```bash
ls -la test_event_portal/
# Should show all folders
```

---

## **Step 4: Test Agent 2 (3-5 minutes)**

```bash
python 02_markdown_generator_agent.py \
  --project "Event Registration Portal" \
  --type frd \
  --output-dir ./test_docs

# Expected output:
# 🚀 MARKDOWN DOCUMENTATION GENERATOR AGENT
# ========================================
# Project: Event Registration Portal
# 📝 Generating FRD for: Event Registration Portal
# 🔄 Asking Qwen to generate content...
# ✅ Code generated successfully
#    ✅ Saved: ./test_docs/01_FRD.md
# ✅ Generated 1 files
```

**Verify:**
```bash
cat test_docs/01_FRD.md
# Should show FRD document
```

---

## **Step 5: Test Agent 3 (3-5 minutes)**

```bash
python 03_code_generator_executor_agent.py \
  --prompt "Write a function to reverse a string" \
  --language python \
  --output test_reverse.py \
  --auto-run

# Expected output:
# 🚀 CODE GENERATOR & EXECUTOR AGENT
# ========================================
# Language: PYTHON
# Prompt: Write a function to reverse a string
# 🔄 Asking Qwen to generate code...
# ✅ Code generated successfully
# 
# Generated Code:
# ─────────────────────────────────
# def reverse_string(s):
#     """Reverse a string."""
#     return s[::-1]
#
# if __name__ == "__main__":
#     ...
# ─────────────────────────────────
#
# ✅ Code saved to: test_reverse.py
# 🐍 Running Python code...
# ─────────────────────────────────
# Original: Hello World
# Reversed: dlroW olleH
# ─────────────────────────────────
```

---

## **If Something Goes Wrong**

### **Problem: "Cannot connect to Ollama"**
```
Solution: Make sure ollama serve is running in Terminal 1
```

### **Problem: "Model not found"**
```
Solution: Run: ollama pull qwen2.5-coder:7b (takes 5-10 min)
```

### **Problem: "Timeout" or Very Slow**
```
Normal! Qwen takes 2-3 minutes per response on CPU.
This is expected and OK for your session.
```

### **Problem: "Invalid JSON"**
```
The example_structure.json may be corrupted.
Try Agent 1 with --generate-from-qwen instead:

python 01_directory_creator_agent.py \
  --generate-from-qwen \
  --prompt "Create directory structure for Flask app" \
  --project test_app
```

---

## **Full Test Sequence (10 minutes)**

```bash
# 1. Start Ollama (Terminal 1)
ollama serve

# 2. In Terminal 2, verify model
ollama list

# 3. Test Agent 1 (JSON input)
python 01_directory_creator_agent.py \
  --json example_structure.json \
  --project test1

# Wait 30 seconds...
ls -la test1/

# 4. Test Agent 2 (Generate FRD)
python 02_markdown_generator_agent.py \
  --project "My Test Project" \
  --type frd \
  --output-dir ./test_docs

# Wait 3-5 minutes...
cat test_docs/01_FRD.md

# 5. Test Agent 3 (Generate code)
python 03_code_generator_executor_agent.py \
  --prompt "Print numbers 1 to 10" \
  --language python \
  --output test.py \
  --auto-run

# Wait 3-5 minutes...
```

---

## **Cleanup (Optional)**

```bash
# Remove test files
rm -rf test_event_portal/
rm -rf test_docs/
rm test_reverse.py
rm test.py
```

---

## **Ready for Session?**

✅ If all 3 agents work → **You're ready!**

✅ Create a folder for your session materials:
```bash
mkdir session_materials
cp 01_directory_creator_agent.py session_materials/
cp 02_markdown_generator_agent.py session_materials/
cp 03_code_generator_executor_agent.py session_materials/
cp example_structure.json session_materials/
cp AGENTS_USAGE_GUIDE.md session_materials/
```

✅ During session, just run the agents from `session_materials/`

---

## **Session Day: Test Again (5 minutes before)**

```bash
# Make sure Ollama is still running
ollama serve

# Quick test one agent
python 01_directory_creator_agent.py --json example_structure.json --project demo
# Should complete in 30 seconds

# You're live!
```

---

**That's it! You're ready for your session.**
