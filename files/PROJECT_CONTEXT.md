# PROJECT CONTEXT — AI Marketing Analytics Dashboard

> This file is the single source of truth for this project.
> Paste this at the start of any new AI conversation to restore full context instantly.

---

## WHO I AM

- **Role:** Digital Marketer, 5+ years experience (in-house + agency)
- **Current:** In-house at a fintech company in Japan (block layoff situation — using time to upskill)
- **Languages:** Japanese and English (both fluent)
- **Location:** Japan
- **Education:** Master's in Japan, Bachelor's in USA
- **Coding level:** Beginner–intermediate (completed The Odin Project foundations + Learn Python the Hard Way)
- **OS:** Linux
- **Background tools:** ChatGPT (heavy user), Looker/Looker Studio, Meta Ads, Google Ads, DV360, X Ads

---

## THE PROJECT

### Name
`marketing-analytics-ai` *(working title)*

### Problem Statement
Marketing data lives across multiple platforms (Meta, Google Ads, DV360, X). Attribution models vary by company. Existing tools like Looker work but feel heavy and inflexible for ad-hoc analysis. There's no easy way to *interpret* data — only display it.

### Solution
A lightweight Python-based marketing analytics tool that:
1. Ingests normalized marketing data (mock data first, real APIs later)
2. Visualizes performance across channels
3. Uses AI (Claude API) to interpret the data in plain language
4. Outputs summaries a marketer can use directly (for reports, Slack, manager updates)

### Target Platforms (data sources)
- Meta Ads
- Google Ads
- DV360
- X (Twitter) Ads

### Stack
- **Language:** Python
- **Data:** Pandas, mock CSV/JSON data (real APIs added later)
- **Visualization:** Matplotlib or Plotly
- **AI layer:** Claude API (claude-sonnet)
- **Interface:** CLI first, simple web UI later (Streamlit or Flask)
- **Version control:** Git + GitHub

### Current Phase
> Phase 1 — Build with mock data. No real company data used.

---

## PROJECT GOALS

1. **Learn by building** — understand AI integration hands-on
2. **Portfolio piece** — something concrete to show recruiters
3. **Eventually monetizable** — solve a real pain point other marketers have
4. **Transferable system** — document everything so the approach can be reused

---

## FOLDER STRUCTURE (planned)

```
marketing-analytics-ai/
├── data/
│   ├── mock/          # Synthetic data mimicking real API responses
│   └── schemas/       # JSON schemas showing real API response shapes
├── src/
│   ├── ingest.py      # Data loading and normalization
│   ├── analyze.py     # Core analysis logic
│   ├── visualize.py   # Chart generation
│   └── ai_layer.py    # Claude API integration
├── prompts/
│   └── system.md      # System prompts for the AI layer
├── notebooks/         # Jupyter notebooks for exploration
├── tests/
├── docs/              # Additional documentation
├── PROJECT_CONTEXT.md # ← This file
├── AI_PROMPTING.md    # Prompting guide and best practices
├── CHANGELOG.md       # What changed and when
└── README.md          # Public-facing project description
```

---

## HOW TO USE THIS FILE

**At the start of a new AI session**, paste this message:

```
Here is my project context: [paste PROJECT_CONTEXT.md contents]

Today I want to work on: [describe your specific task]
```

That's it. The AI will have full context without you re-explaining everything.

**Update this file whenever:**
- The project scope changes
- You finish a phase
- You add a new tool or platform
- Your goals shift

---

## CURRENT STATUS

- [ ] Project folder created
- [ ] Mock data schemas defined
- [ ] Mock data generator written
- [ ] Basic data ingestion working
- [ ] First visualization working
- [ ] Claude API integrated
- [ ] First AI summary generated
- [ ] README written for GitHub
- [ ] Deployed / shareable link

---

*Last updated: 2026-04-06*
