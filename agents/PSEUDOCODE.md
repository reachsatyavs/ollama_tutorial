# 📘 Agent Pseudocode (for teaching)

Plain-English pseudocode for the three agents in this folder. Use it to explain to students
*what each agent does* without getting lost in Python syntax.

> ### The one pattern that unites all three agents
>
> Every agent — and every agent you will ever build — is the same three-step loop:
>
> ```
>   1. BUILD a prompt        (turn the user's request into instructions for the model)
>   2. ASK the local model   (send prompt to Ollama at http://localhost:11434)
>   3. ACT on the reply      (do something real: make folders / save files / run code)
> ```
>
> A *model* stops after step 2 (it only returns text). An *agent* adds step 3 — it **acts**.

A shared helper used by all three:

```
FUNCTION ASK_MODEL(prompt):
    # This is the only place we talk to the AI.
    reply = HTTP POST to "http://localhost:11434/api/generate"
            with body { model: "qwen2.5-coder:7b", prompt: prompt, stream: false }
    RETURN reply.response          # the text the model generated
```

---

## 🗂️ Agent 1 — Directory Structure Creator
File: [`01_directory_creator_agent.py`](01_directory_creator_agent.py)

**Purpose:** turn a project idea into real folders on disk.

**Inputs:** a project name, and EITHER a JSON file describing the folders OR a text prompt
(the model designs the structure).

```
PROGRAM DirectoryCreatorAgent

MAIN(project_name, json_file, prompt):

    # STEP 1 + 2 — get the folder structure (as a nested object)
    IF user chose "generate from model":
        full_prompt = prompt + "Reply with ONLY the structure as JSON"
        raw_text    = ASK_MODEL(full_prompt)
        structure   = EXTRACT_JSON(raw_text)      # find the {...} and parse it
    ELSE IF a JSON file was given:
        structure   = READ_AND_PARSE(json_file)
    ELSE:
        STOP "need either --json or --generate-from-qwen"

    # STEP 3 — ACT: create the folders on disk
    CREATE_FOLDERS(structure, root = project_name)
    CREATE_INIT_FILES(["src", "tests", "config"])   # add empty __init__.py
    PRINT how many folders were created and where


FUNCTION CREATE_FOLDERS(structure, current_path):
    FOR EACH (name, children) IN structure:
        path = current_path + "/" + name
        MAKE_DIRECTORY(path)                         # the real action
        IF children is a non-empty object:
            CREATE_FOLDERS(children, path)           # recurse into subfolders


FUNCTION EXTRACT_JSON(text):
    # the model sometimes adds chatter around the JSON
    cut = text from the first "{" to the last "}"
    RETURN PARSE_JSON(cut)
```

> 🐞 **Note for students:** every key in the JSON is treated as a *folder*. So an entry like
> `"app.py"` becomes a **folder named app.py**, not a file. (A nice "spot the bug" exercise.)

---

## 📝 Agent 2 — Markdown Documentation Generator
File: [`02_markdown_generator_agent.py`](02_markdown_generator_agent.py)

**Purpose:** ask the model to write project documents (FRD, use cases, test cases, class diagram)
and save each as a markdown file.

**Inputs:** a project name/description, which document type(s) to make (`frd`, `usecases`,
`testcases`, `classdiagram`, or `all`), and an output directory.

```
PROGRAM MarkdownGeneratorAgent

MAIN(project_name, doc_type, output_dir):

    # decide which documents to produce
    IF doc_type == "all":
        types = ["frd", "usecases", "testcases", "classdiagram"]
    ELSE:
        types = [doc_type]

    FOR EACH type IN types:
        # STEP 1 — build a prompt from a template for this document type
        prompt  = BUILD_PROMPT(type, project_name)

        # STEP 2 — ask the model
        content = ASK_MODEL(prompt)

        # STEP 3 — ACT: save the reply as a .md file
        IF content is not empty:
            SAVE_TO_FILE(output_dir, numbered_name(type), content)

    PRINT how many files were saved and where


FUNCTION BUILD_PROMPT(type, project):
    # each document type has its own instruction template, e.g.
    #   frd          -> "write overview, objectives, roles, features, requirements, database"
    #   usecases     -> "write 4-6 use cases with actor, precondition, steps, postcondition"
    #   testcases    -> "write 5-8 test cases with id, steps, expected result, status"
    #   classdiagram -> "write a Mermaid classDiagram with classes, properties, methods"
    RETURN the matching template, filled in with `project`
```

> 🐞 **Note for students:** the request body currently sets `stream: true`, but the code then
> tries to read the whole reply at once. Streaming returns the answer in many small pieces, so
> this combination will error — it should be `stream: false`. Good real-world debugging lesson.
> (Also: the `--custom-prompt` option is accepted but never actually used.)

---

## 💻 Agent 3 — Code Generator & Executor
File: [`03_code_generator_executor_agent.py`](03_code_generator_executor_agent.py)

**Purpose:** ask the model to write a program, check it for obviously dangerous operations,
save it, and optionally run it.

**Inputs:** a prompt describing the code, a language (`python` or `javascript`), an output file,
and flags: `--auto-run`, `--no-save`, `--input`.

```
PROGRAM CodeGeneratorExecutorAgent

MAIN(prompt, language, output_file, auto_run, no_save, input_data):

    # STEP 1 — wrap the request in clear instructions
    full_prompt = "Write a complete, runnable " + language +
                  " program for: " + prompt + " (return ONLY the code)"

    # STEP 2 — ask the model
    raw_text = ASK_MODEL(full_prompt)

    # clean the reply: strip ``` code fences if present
    code = EXTRACT_CODE(raw_text)

    # SAFETY GATE — refuse anything with dangerous operations
    IF NOT SECURITY_CHECK(code):
        STOP "blocked for safety"

    SHOW code to the user

    # STEP 3 — ACT: save and/or run
    IF should save:
        WRITE code TO output_file

    IF auto_run OR user answers "yes":
        RUN_CODE(code, language, input_data)     # 30-second time limit
        PRINT the program's output


FUNCTION SECURITY_CHECK(code):
    BLOCKED = [ "os.remove", "os.system", "shutil.rmtree",
                "subprocess.call", "eval(", "exec(", ... ]
    FOR EACH keyword IN BLOCKED:
        IF keyword appears in code:
            RETURN unsafe
    RETURN safe


FUNCTION EXTRACT_CODE(text):
    IF text contains a ```language ... ``` block:
        RETURN the text inside the fences
    ELSE:
        RETURN text unchanged
```

> ⚠️ **Note for students:** `SECURITY_CHECK` is a simple keyword blocklist, **not** a real sandbox.
> It's easy to bypass. Never run AI-generated code you haven't read. Teaching guard only.

---

### 🧠 Summary to leave students with

| Agent | Prompt asks the model for… | The real ACTION it takes |
|-------|----------------------------|--------------------------|
| **1** | a folder layout (JSON) | creates directories on disk |
| **2** | document text (markdown) | saves `.md` files |
| **3** | a program (code) | saves and runs the code |

Same brain (the model), three different hands (the actions). **That is what an agent is.**
