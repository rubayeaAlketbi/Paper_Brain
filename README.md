# Paper-Brain: Your Personal AI Research Assistant

A local-first CLI tool that discovers, summarizes, organizes, and connects research papers into a **second brain** for research analysts. Built to teach AI engineering fundamentals while solving a real problem.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)

---

## Quick Start

### Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/paper-brain.git
cd paper-brain

# Install in editable mode
pip install -e .

# Verify it works
brain --help
```

### Set up your API keys

```bash
# Create a .env file in the project root
cat > .env << EOF
S2_API_KEY=your_semantic_scholar_api_key_here
ANTHROPIC_API_KEY=your_claude_api_key_here
PAPER_BRAIN_DATA=~/.paper-brain
EOF

# Load it (or export manually)
export $(cat .env | xargs)

# Verify
brain --help
```

### Your first paper

```bash
# Add a paper from arXiv or Semantic Scholar
brain add arxiv:2312.10997

# Summarize it
brain summarize arxiv:2312.10997

# List all papers
brain list

# Search your library
brain search "diffusion models"
```

---

## What it does (today and roadmap)

| Phase | Feature | Status | What you learn |
|-------|---------|--------|----------------|
| **0** | Installable skeleton | ✓ Done | Python packaging, typer CLI, 12-factor config |
| **1** | Ingest & store | → In progress | REST APIs, PDF parsing, data modeling |
| **2** | Structured summarization | → Next | Prompt engineering, structured LLM output, evaluation |
| **3** | Search & organize | 📋 Planned | Embeddings, vector search, nearest-centroid classification |
| **4** | Daily nominations | 📋 Planned | Recommender systems, scheduling, idempotent pipelines |
| **5** | Knowledge graph | 📋 Planned | Graph data structures, visualization, concept extraction |
| **6** | Framework comparison | 📋 Planned | LlamaIndex/LangChain internals vs. first-principles |

---

## Project structure

```
paper-brain/
├── README.md                          # ← You are here
├── pyproject.toml                     # Package metadata + dependencies
├── .env                               # (gitignored) Your API keys
│
├── src/paper_brain/
│   ├── __init__.py
│   ├── cli.py                         # typer app, command routing
│   ├── config.py                      # env var loading
│   │
│   ├── ingest.py                      # Phase 1: fetch, parse, store
│   ├── summarize.py                   # Phase 2: LLM → structured note
│   ├── embed.py                       # Phase 3: embeddings & search
│   │
│   ├── store.py                       # LanceDB interface (THE choke point)
│   └── discover.py                    # Phase 4: daily nominations
│
├── notes/                             # Output: Markdown notes per topic
│   └── llms/
│       └── 2026-07-20-attention-is-all-you-need.md
│
├── pdfs/                              # Raw PDFs (not in git)
│   └── arxiv-2312.10997.pdf
│
├── data/
│   └── lancedb/                       # Vector DB (not in git)
│       └── papers.db
│
└── tests/                             # Unit + integration tests
    └── test_ingest.py
```

---

## Architecture overview

```
┌──────────────────────────────────────────┐
│ Semantic Scholar API + arXiv API         │
│ (metadata, TLDRs, citations, PDFs)       │
└──────────────────┬───────────────────────┘
                   │
        ┌──────────▼─────────┐
        │   Ingest module    │ fetch → parse → store
        └──────────┬─────────┘
                   │
        ┌──────────▼──────────────┐
        │  Summarize module       │ structured LLM call
        │  (Claude via API)       │ → 6-section note
        └──────────┬──────────────┘
                   │
        ┌──────────▼──────────┐
        │  Embed module       │ local sentence-transformers
        └──────────┬──────────┘
                   │
     ┌─────────────┼──────────────┐
     ▼             ▼              ▼
  LanceDB        notes/         pdfs/
  (vectors +   (Markdown)      (raw)
   metadata)
```

**Every paper becomes:**
1. One row in LanceDB (metadata + vector)
2. One Markdown note in `notes/<topic>/YYYY-MM-DD-<slug>.md`
3. One PDF in `pdfs/<paper_id>.pdf`

---

## Core data model (LanceDB)

| column | type | meaning |
|--------|------|---------|
| `paper_id` | str (PK) | Semantic Scholar canonical ID |
| `arxiv_id`, `doi` | str | keep originals for traceability |
| `title`, `abstract`, `authors` | str / list | basic metadata |
| `year`, `venue` | int / str | publication context |
| `citation_count` | int | refreshed periodically |
| `topic` | str | auto-assigned to folder in Phase 3 |
| `status` | str | "inbox" \| "summarized" \| "read" |
| `added_at`, `updated_at` | timestamp | sortable by date |
| `note_path` | str | where the Markdown lives |
| `vector` | vector(384) | embedding of abstract+summary |
| `summary_json` | JSON | 6-section structured summary |

One table, one embedded DB file, no server. `store.py` is the only module allowed to write to it — this boundary is itself a design pattern (repository pattern).

---

## The note template

Every paper gets `notes/<topic>/YYYY-MM-DD-<slug>.md`:

```markdown
---
paper_id: 204e3073870fae3d05bcbc2f6a8e263d9b72e776
title: Attention Is All You Need
authors: [Vaswani, Shazeer, ...]
year: 2017
topic: transformers
tags: [nlp, attention, architecture]
added_at: 2026-07-20T14:32:00Z
---

# Attention Is All You Need

## Summary
<!-- Machine-generated: one sentence overview -->

## Problem
<!-- What pain point does this paper address? -->

## Solution
<!-- Core technical contribution -->

## Implementation
<!-- How did they build it? Key algorithms/hyperparameters -->

## Key Takeaway
<!-- The one idea you'll remember in 6 months -->

## Significance in the Research Area
<!-- Why does this matter for the field? -->

---

## My Notes
<!-- This section is yours — the pipeline never touches it.
     Add your reactions, related papers, open questions, or "hmm this
     contradicts paper X, worth investigating". -->
```

The **My Notes** section is protected: the ingest pipeline writes above it, never overwriting your thinking.

---

## Development setup

### Install for development

```bash
# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### (Future) Run tests

```bash
pytest tests/
```

### Before committing code

```bash
# Format
black src/ tests/

# Lint
ruff check src/ tests/ --fix

# Type check
mypy src/
```

---

## How to use this as a learning project

Each phase is designed to teach you one AI-engineering concept from first principles:

1. **Phase 1 (Ingest):** Start here. You'll hit the real-world messiness of "I have 1000s of PDFs in different formats" — this is where most tutorials skip the learning.

2. **Phase 2 (Summarize):** Learn prompt engineering by hand-tuning summaries on 10 papers. Grade yourself. See what works.

3. **Phase 3 (Embeddings):** Write cosine similarity from scratch with NumPy. Understand it. *Then* switch to LanceDB's ANN index and measure the difference.

4. **Phase 6 (Framework comparison):** Rebuild one phase with LangChain or LlamaIndex. Write a short comparison (what it hid, what it saved). That's your portfolio piece.

See `LEARNING.md` for a concept syllabus and "rebuild test" guidance.

---

## Configuration

Environment variables (load from `.env`):

| Variable | Required? | Default | Meaning |
|----------|-----------|---------|---------|
| `S2_API_KEY` | Yes | — | Semantic Scholar API key (free, sign up at https://www.semanticscholar.org/product/api) |
| `ANTHROPIC_API_KEY` | Yes | — | Claude API key (https://console.anthropic.com) |
| `PAPER_BRAIN_DATA` | No | `~/.paper-brain` | Where to store notes, PDFs, LanceDB |
| `LOG_LEVEL` | No | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

---

## Roadmap & known limitations

### Current limitations
- Only open-access PDFs (no paywalled papers yet)
- Semantic Scholar's recommendations API covers only papers from the last 60 days
- No user authentication (single-user local tool)
- No cloud sync (by design, for now)

### Future
- Web UI (Phase 7)
- RAG chat: "ask your library a question" (Phase 7)
- Zotero/Mendeley import
- Multi-device sync via S3/git
- Custom topic hierarchies

---

## Contributing

This is a personal learning project, but if you fork it:

1. Each commit should pass `black`, `ruff`, and `mypy`
2. Add a test for any new module
3. Update this README if you change the structure
4. Document your learning in `LEARNING.md` — especially if you rebuilt a phase with a framework

---

## How Claude can help organize this repo

Claude can review and improve:
- **Code quality:** type hints, docstrings, function organization
- **Module boundaries:** does `store.py` actually stay as the single "write" choke point?
- **Test coverage:** what tests are missing?
- **Documentation:** are the comments clear for someone reading your code 6 months from now?
- **Architecture:** "Does the data model need a change before we go too far?"

See **"Granting Claude access"** section below.

---

## Granting Claude access to your repo

You have two main options:

### Option 1: GitHub + Claude's GitHub MCP (easiest)

1. Push your repo to GitHub (public or private)
2. In Claude.ai or Claude Desktop, enable the GitHub connector
3. Ask Claude: "Review the architecture of my paper-brain repo" or "refactor the store.py module"

Claude will:
- Read your files
- Understand the structure
- Suggest improvements
- In some cases, create draft PRs

**Pros:** No setup, Claude sees your live code, can propose PRs.  
**Cons:** Your repo is on GitHub; requires you to authenticate Claude with your GitHub account.

### Option 2: Local file access via Claude Desktop (most private)

1. Install Claude Desktop (https://claude.ai/download)
2. Open your repo folder in Claude Desktop
3. Ask Claude to help organize; it has access to all files locally

**Pros:** Everything stays on your machine; no GitHub account needed.  
**Cons:** Only works in Claude Desktop, not claude.ai.

### Option 3: Copy-paste into this chat (simplest start)

1. Share your repo structure: `tree -I '__pycache__|*.egg-info' paper-brain/`
2. Paste key files (cli.py, store.py, etc.)
3. Ask for feedback

**Pros:** Works now, no setup.  
**Cons:** Manual; limited to what fits in the chat.

---

## Recommended first steps for Claude help

**Once your Phase 0 skeleton is ready**, ask Claude:

> "I'm at Phase 1 now. Here's my project structure and my ingest.py. 
> Before I build further, review:
> 1. Are my module boundaries clean?
> 2. Is store.py ready to be the single write choke point?
> 3. What's missing from my error handling?
> 4. Should I add type hints anywhere?"

This way Claude becomes a **code reviewer** early, not a "fix everything at the end" tool.

---

## License

MIT — see LICENSE file.

---

## Questions?

- Architecture: See `paper-brain-blueprint.md` in `/vault/projects/paper-brain/`
- Learning syllabus: See `LEARNING.md` (coming)
- API reference: Semantic Scholar docs at https://www.semanticscholar.org/product/api
- Claude API: https://docs.anthropic.com

---

**Built as a learning project by [your name] in 2026.**  
*This tool is designed to teach AI engineering while solving a real research problem.*
