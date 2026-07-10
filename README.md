# 🦙 Ollama Tutorial — Run AI Models Locally & Build Simple Agents

> **The big idea:** You don't need a paid cloud subscription (ChatGPT Plus, Claude Pro, etc.)
> to get real work done with AI. You can run capable models **on your own laptop**, for free,
> fully offline — and even wire them into small programs ("agents") that do useful things like
> scaffolding a project, writing documentation, or generating code.
>
> This repo teaches you how, step by step, with **three working example agents** you can run today.

---

## 📚 Table of Contents

1. [Who this is for & what you'll learn](#-who-this-is-for)
2. [Core concepts — AI, LLM, SLM, Model, Agent](#-core-concepts)
3. [Local vs Cloud — why run models on your own machine?](#-local-vs-cloud)
4. [Minimum system requirements](#-minimum-system-requirements)
5. [Step 1 — Install Ollama](#-step-1--install-ollama)
6. [Step 2 — Download a model & ask it questions](#-step-2--download-a-model--ask-it-questions)
7. [Step 3 — Install Python with uv](#-step-3--install-python-with-uv)
8. [Step 4 — Get this repo](#-step-4--get-this-repo)
9. [Model vs Agent — what's the difference?](#-model-vs-agent--the-key-difference)
10. [The three example agents](#-the-three-example-agents)
11. [A full example workflow](#-a-full-example-workflow)
12. [Troubleshooting](#-troubleshooting)

---

## 👋 Who this is for

Students, hobbyists, and developers who want to **use AI without a monthly bill**. If you can
open a terminal and type commands, you can do this. No machine-learning background needed.

**By the end you will be able to:**

- Explain what AI, LLMs, SLMs, models, and agents actually are.
- Install Ollama and run a language model **locally** on Mac or Windows.
- Chat with a model from your terminal, completely offline.
- Run three small Python "agents" that use a local model to **create folders, write docs, and generate code**.

---

## 🧠 Core Concepts

Let's define the words you'll keep hearing. Plain English, no jargon.

### AI (Artificial Intelligence)
The broad field of making computers do things that normally need human intelligence —
understanding language, recognizing images, making decisions. It's the *umbrella term*.
Everything below is a piece of AI.

### Model
A **model** is the "brain" — a big file full of numbers (called *weights*) that has learned
patterns from huge amounts of data. On its own a model just does one thing: **given some input
text, predict the next words.** It has no memory, no tools, no goals. It's like a very
well-read parrot: give it a prompt, it gives you text back.

> In this tutorial, `qwen2.5-coder:7b` is a **model** — a 4.7 GB file you download once.

### LLM (Large Language Model)
A model **trained on text** to understand and generate human language. "Large" because it has
billions of parameters (weights). Examples: GPT-4, Claude, Llama 3, Qwen. They're powerful but
big — the largest ones need data-center hardware, which is why they usually live in the cloud.

### SLM (Small Language Model)
The same idea as an LLM, just **smaller** (a few hundred million to ~7 billion parameters).
The trade-off: an SLM is a little less "smart" than a giant model, but it's small enough to run
on a **regular laptop**, fast and free. SLMs are the sweet spot for local, everyday tasks —
scaffolding a project, drafting docs, writing a function.

> `qwen2.5-coder:7b` (7 billion parameters) is a small/mid model that runs comfortably on a
> normal laptop. That's the whole point.

### Ollama
A free tool that makes running models locally **easy**. It downloads models, runs them, and
gives you both a chat prompt and a local API (`http://localhost:11434`) that your programs can
call. Think of it as "Docker for AI models."

### Agent
An **agent** is a model **plus code that lets it take actions.** A raw model can only produce
text. An agent wraps that text in a program that *does something with it* — creates files, runs
commands, calls other tools, loops until a goal is met. (More on this [below](#-model-vs-agent--the-key-difference).)

> The three programs in this repo are **agents**: they ask the local model for text, then act
> on that text — making directories, saving markdown, or running generated code.

---

## ⚖️ Local vs Cloud

Why run models on your own machine instead of using a cloud service?

### ✅ Advantages of running locally
- **Free** — no subscription, no per-token billing. Run it a million times, still $0.
- **Private** — your prompts and data never leave your computer. Nothing is sent to a company's servers.
- **Offline** — works on a plane, in a basement, with no internet.
- **No rate limits** — hammer it as hard as your hardware allows.
- **Always available** — no outages, no "we've changed our terms," no deprecated models.
- **Great for learning** — see exactly how the pieces fit together, tweak everything.

### ⚠️ Risks & downsides of the cloud
- **Cost** — monthly subscriptions and usage bills add up.
- **Privacy** — your data goes to a third party; it may be logged, cached, or used for training.
- **Dependency** — outages, price hikes, or a discontinued model can break your workflow overnight.
- **Internet required** — no connection, no AI.
- **Rate limits & quotas** — you can be throttled or cut off mid-task.

### ❌ Downsides of running locally (be honest)
- **Less raw power** — a 7B local model is not as capable as a giant frontier cloud model for
  hard reasoning or very long documents.
- **Uses your hardware** — needs enough RAM; older or low-memory machines will be slow.
- **Speed** — on a CPU-only machine, responses can take 1–3 minutes. (Apple Silicon and GPUs are much faster.)
- **You manage it** — you download models, update tools, and free up disk space yourself.

**The honest takeaway:** Use **local models** for everyday, private, high-volume tasks where
"good enough and free" wins (exactly what this repo demos). Reach for a **cloud model** when you
need maximum capability on a hard, one-off problem. Many people use both.

---

## 💻 Minimum System Requirements

Ollama runs on **macOS, Windows, and Linux**. Model size drives the requirements — bigger models
need more RAM.

| Your RAM | What you can run | Example models |
|----------|------------------|----------------|
| **8 GB** | Small models (1B–3B) | `qwen3.5:0.8b`, `ministral-3:3b`, `llama3.2:3b` |
| **16 GB** ✅ | Mid models (7B) — **recommended for this tutorial** | `qwen2.5-coder:7b` |
| **32 GB+** | Larger models (13B–34B) | `qwen2.5-coder:14b`, `codellama:34b` |

**General guidance:**
- **macOS:** Apple Silicon (M1/M2/M3/M4) is excellent — the GPU and RAM are shared ("unified memory"), so models run fast. Intel Macs work but are slower. macOS 12+.
- **Windows:** Windows 10/11. A dedicated NVIDIA GPU makes it much faster, but it's optional — it'll run on CPU too, just slower.
- **Disk:** each model is a few GB. `qwen2.5-coder:7b` is ~4.7 GB. Keep 10+ GB free.
- **No GPU?** Everything still works on CPU — just expect slower responses.

> This tutorial is tuned for `qwen2.5-coder:7b`. On 8 GB RAM, swap in a smaller model like
> `ministral-3:3b` (see how in [The three example agents](#-the-three-example-agents)).

---

## 🚀 Step 1 — Install Ollama

### macOS
**Option A — Homebrew (recommended):**
```bash
brew install ollama
```
**Option B — Download the app:** grab it from [ollama.com/download](https://ollama.com/download) and drag it to Applications.

### Windows
Download the installer from [ollama.com/download](https://ollama.com/download) and run it. That's it — Ollama starts automatically and lives in your system tray.

### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Verify it worked
```bash
ollama --version
```

### Start the Ollama server
Ollama needs a background server running (it exposes the local API at `http://localhost:11434`).

- **Windows / macOS app:** it starts automatically when you launch Ollama.
- **From the terminal (any OS):**
  ```bash
  ollama serve
  ```
  Leave this running in its own terminal window. Open a **second** terminal for the commands below.

---

## 💬 Step 2 — Download a Model & Ask It Questions

Download the model this tutorial uses (~4.7 GB, one-time):
```bash
ollama pull qwen2.5-coder:7b
```

See what you have:
```bash
ollama list
```

**Now chat with it — fully offline, no account, no bill:**
```bash
ollama run qwen2.5-coder:7b
```
You'll get a prompt. Try:
```
>>> Explain what a REST API is in two sentences.
>>> Write a Python function that checks if a number is prime.
>>> /bye        # type this to exit
```

🎉 **That's a language model running entirely on your machine.** No internet required after the download.

**Prefer a smaller/faster model?** (good for 8 GB RAM):
```bash
ollama pull ministral-3:3b
ollama run ministral-3:3b
```

---

## 🐍 Step 3 — Install Python with uv

The three agents are Python programs. We use **[uv](https://docs.astral.sh/uv/)** — a modern,
extremely fast tool that installs Python *and* manages the project's dependencies for you. No
need to fuss with `pip`, `venv`, or which Python version you have.

### Install uv

**macOS / Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
(Or on a Mac with Homebrew: `brew install uv`)

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Verify:
```bash
uv --version
```

That's it — uv will download the correct Python and packages **automatically** the first time you
run an agent (Step 4). You never have to install Python separately.

---

## 📥 Step 4 — Get This Repo

```bash
git clone <your-repo-url> ollama_tutorial
cd ollama_tutorial

# Install Python + dependencies automatically (uv reads pyproject.toml)
uv sync
```

`uv sync` creates a local environment and installs the one dependency (`requests`). Done.

Run any agent with `uv run` — this guarantees the right Python and packages are used:
```bash
uv run agents/01_directory_creator_agent.py --help
```

> **Tip:** always launch the agents with `uv run` (not a bare `python`). It uses the project's
> managed environment, which also ensures `python` is on the PATH for Agent 3's code execution.

---

## 🤖 Model vs Agent — the Key Difference

This is the most important concept in the whole tutorial.

| | **Model** | **Agent** |
|---|-----------|-----------|
| **What it is** | The "brain" — predicts text | A **program** that uses the brain to *act* |
| **Can it act?** | ❌ No. Only outputs text. | ✅ Yes — creates files, runs code, calls tools |
| **Memory / goals?** | ❌ None | ✅ Has a task it works toward |
| **Example** | `qwen2.5-coder:7b` | `01_directory_creator_agent.py` |

**Analogy:** A **model** is a brilliant author locked in a room who can only slide written notes
under the door. An **agent** is the assistant standing outside who *reads those notes and does
what they say* — files the paperwork, builds the shelf, runs the errand.

**In this repo:** each agent sends a prompt to your local model via Ollama's API, gets text back,
and then **does something real with it** — makes directories on disk, saves markdown files, or
executes generated code. The model thinks; the agent acts.

---

## 🛠️ The Three Example Agents

All three call your **local** model at `http://localhost:11434` — no cloud, no cost.

> **New to this? Start with the tiny example first:** [`examples/simple_agent.py`](examples/simple_agent.py)
> is the smallest possible agent — a model that decides to call one tool (`get_weather`) and acts on
> the result. Run it with `uv run examples/simple_agent.py`. There's also a plain (non-agent) model
> call in [`examples/qwen_hello.js`](examples/qwen_hello.js) using the JavaScript client.

### Agent 1 — Directory Structure Creator
📄 [`agents/01_directory_creator_agent.py`](agents/01_directory_creator_agent.py)

Turns a project idea into **real folders on disk**. Either give it a JSON layout, or ask the model
to design one for you.

```bash
# From a ready-made JSON layout (instant)
uv run agents/01_directory_creator_agent.py \
  --json examples/example_structure.json \
  --project my_first_app

# Or let the model design the structure for you
uv run agents/01_directory_creator_agent.py \
  --generate-from-qwen \
  --prompt "Directory structure for a Flask event-registration website" \
  --project event_portal
```

### Agent 2 — Markdown Documentation Generator
📄 [`agents/02_markdown_generator_agent.py`](agents/02_markdown_generator_agent.py)

Asks the model to write project docs — a Functional Requirements Doc, use cases, test cases, and a
class diagram — and saves them as markdown files.

```bash
uv run agents/02_markdown_generator_agent.py \
  --project "Event Registration Portal" \
  --type all \
  --output-dir ./event_portal/docs
```

### Agent 3 — Code Generator & Executor
📄 [`agents/03_code_generator_executor_agent.py`](agents/03_code_generator_executor_agent.py)

Asks the model to write a program, saves it, runs a basic safety check, and can execute it for you.

```bash
uv run agents/03_code_generator_executor_agent.py \
  --prompt "A function to reverse a string, with a demo" \
  --language python \
  --output reverse.py \
  --auto-run
```
> ⚠️ **Always read generated code before running it.** Agent 3 has a simple keyword blocklist
> (`os.system`, `eval`, `shutil.rmtree`, …) but it is a teaching guard, **not** a real sandbox.

**Using a different model?** These agents are set to `qwen2.5-coder:7b`. To use another one
(e.g. on a low-RAM machine), open the agent file and change the `"model"` value in the
`requests.post(...)` call to whatever `ollama list` shows (e.g. `"ministral-3:3b"`).

---

## 🎬 A Full Example Workflow

The philosophy of this repo in action: **ask the model to do the boring scaffolding, then you
take over the interesting part.**

```bash
# 1) Ask the model to design & create a project skeleton
uv run agents/01_directory_creator_agent.py \
  --generate-from-qwen \
  --prompt "Directory structure for a task-tracker web app" \
  --project task_tracker

# 2) Ask it to draft the documentation
uv run agents/02_markdown_generator_agent.py \
  --project "Task Tracker Web App" \
  --type all \
  --output-dir ./task_tracker/docs

# 3) Ask it for a starter function — then YOU refine it
uv run agents/03_code_generator_executor_agent.py \
  --prompt "A function that adds a task with a title and due date to a list" \
  --language python \
  --output task_tracker/add_task.py
```

In minutes you've gone from an idea to a folder structure, docs, and starter code — **all for free,
all offline.** From here, you open the files in your editor and build the real thing.

---

## 🔧 Troubleshooting

**"Cannot connect to Ollama" / connection refused**
The server isn't running. Start it: `ollama serve` (or launch the Ollama app), then retry.

**"model not found"**
Download it: `ollama pull qwen2.5-coder:7b`. Check with `ollama list`.

**Responses are very slow (1–3 minutes)**
Normal on CPU-only machines. Use a smaller model (`ministral-3:3b`) or be patient. Apple Silicon and NVIDIA GPUs are much faster.

**`python: command not found` (when Agent 3 runs code)**
Launch agents with `uv run` — it puts the right `python` on the PATH.

**Out of memory / machine freezes**
The model is too big for your RAM. Switch to a smaller model (see the requirements table).

---

## 📂 Repo Contents

```
ollama_tutorial/
├── README.md                  ← you are here
├── pyproject.toml             ← Python project + dependencies (managed by uv)
├── package.json               ← Node dependency for the JavaScript example
├── agents/                    ← the three example agents
│   ├── 01_directory_creator_agent.py
│   ├── 02_markdown_generator_agent.py
│   └── 03_code_generator_executor_agent.py
└── examples/
    ├── simple_agent.py         ← the smallest possible agent (tool calling) — start here
    ├── qwen_hello.js           ← plain model call via the JavaScript client
    └── example_structure.json  ← sample layout for Agent 1
```

---

**Happy hacking — run models locally, keep your data private, and build. 🦙**
