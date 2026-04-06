# DEVLOG.md — Development Log

> A plain-English record of how this project was built, step by step.
> Updated after every working session.
> Goal: anyone (including future me) can read this and understand not just WHAT was built, but WHY and HOW.

---

## How to use this file

After every session, add a new entry at the top with:
- What you worked on
- What you learned
- What prompts / questions drove the work
- Commands or code worth remembering

---



## SESSION 1 — 2026-04-06

### What we worked on
Project setup — getting the foundation in place before writing any real code.

### STEP 3 — Mock Data Generator
⏱ 2026-04-06 | ~25 min

#### What we did (plain English)

Wrote a Python script (`data/mock/generate_mock_data.py`) that generates 
90 days of fake but realistic marketing data for all 4 platforms.

Output: 4 CSV files, 1,260 rows total
- `data/mock/meta.csv` — 360 rows
- `data/mock/google_ads.csv` — 360 rows
- `data/mock/dv360.csv` — 270 rows
- `data/mock/x_ads.csv` — 270 rows

Date range: 2026-01-01 → 2026-03-31

#### How the script works

1. Defines a date range and fake campaign names per platform
2. For each platform, loops through every date × every campaign
3. Generates random but realistic numbers for each metric
4. Calculates derived metrics (CTR, CPC, CPM, ROAS) from the raw numbers
5. Saves each platform as a CSV

#### Key things the data confirmed

**Google ROAS looks low vs Meta** — realistic. Search campaigns show 
lower in-platform ROAS because of attribution differences. Not a bug, 
a real-world pattern.

**DV360 impressions are much higher** — programmatic display runs at 
high volume, low engagement. Expected.

**X has the cheapest CPMs** — X ad inventory is genuinely cheaper 
than Meta or Google. Data reflects reality.

**Google conversions are decimals (4.1, 9.4)** — this is correct. 
Data-driven attribution splits credit fractionally across touchpoints.

#### What we learned
- Generating mock data forces you to understand what realistic 
  numbers look like per platform
- Derived metrics (CTR = clicks/impressions) should be calculated 
  from raw numbers, not made up independently
- The data already tells a story before any analysis is written

#### Prompts that drove this step

1. *"commited! let's go to step 3"*
   → Led to writing the full mock data generator in one script

---

#### Status after this step
- [x] Mock data generator written
- [x] 1,260 rows of realistic data across 4 platforms
- [x] Data sanity checked and verified
- [ ] Data ingestion + normalization ← next

---

#### Next session starting point
```
Context: marketing-analytics-ai project, Phase 1
Last completed: Step 3 — mock data generator
Next task: Step 4 — ingest all 4 CSVs and normalize into one 
unified table with consistent column names
File to work on: src/ingest.py
Activate venv first: source venv/bin/activate
```

### STEP 2 — Mock Data Schemas

#### What we did (plain English)

Before writing any code that processes data, we needed to understand the *shape* 
of data from each platform. Every ad platform returns different field names, 
different metrics, and different structures. This step defined those blueprints.

We created one JSON schema file per platform in `data/schemas/`:

| File | Platform |
|---|---|
| `meta.json` | Meta Ads |
| `google_ads.json` | Google Ads |
| `dv360.json` | DV360 |
| `x_ads.json` | X Ads |

Each schema documents:
- Every field the API returns
- What data type it is
- The default attribution window for that platform

---

#### Key differences between platforms (this matters later)

**Field naming inconsistencies — same metric, different names:**
| Metric | Meta | Google Ads | DV360 | X Ads |
|---|---|---|---|---|
| Money spent | `spend` | `cost` | `media_cost` | `spend` |
| Campaign unit | `campaign` | `campaign` | `insertion_order` | `campaign` |

This is why we need a normalization layer — before combining data from all 
4 platforms, we need to rename everything to match.

**DV360 has two cost fields:**
- `media_cost` — what you actually pay for ad inventory
- `total_cost` — media cost + platform fees
This trips up a lot of marketers when comparing spend across platforms.

**Google Ads conversions can be decimals:**
Because of data-driven attribution (DDA), Google splits conversion credit 
across multiple touchpoints. You might see 2.4 conversions. Meta always 
shows whole numbers.

**X Ads has the shortest attribution window (1-day click, 1-day view):**
Meta's default is 7-day click. This means the same conversion can be claimed 
by both platforms at the same time — this is the core attribution problem 
this project will eventually help solve.

**X Ads tracks engagements as a unique metric:**
Likes + retweets + replies + clicks bundled into one number. Reflects that 
X isn't purely a direct response channel.

---

#### What we learned
- Every platform has its own vocabulary for the same concepts
- Attribution windows vary widely — this is why cross-platform reporting 
  is always "lying" to some degree
- Schemas first, code second — understanding data shape before touching 
  code saves a lot of refactoring later

#### Prompts / questions that drove this step

1. *"Ready for step 2"*
   → Led to explaining why schemas come before code, and building 
   one schema per platform with commentary on key differences

---

#### Status after this step
- [x] Meta Ads schema defined
- [x] Google Ads schema defined
- [x] DV360 schema defined
- [x] X Ads schema defined
- [x] Key differences between platforms documented
- [ ] Mock data generator written ← next

---

#### Next session starting point
```
Context: marketing-analytics-ai project, Phase 1
Last completed: Step 2 — mock data schemas for all 4 platforms
Next task: Step 3 — write a Python script that generates fake but 
realistic marketing data based on these schemas
Activate venv first: source venv/bin/activate
```
---

### STEP 1 — Project Setup & Environment

#### What we did (plain English)

**1. Created the folder structure**
Built a set of organized directories that give every part of the project a clear home. Think of it like setting up a filing cabinet before you start a big project — you don't want to figure out where things go after the mess has already started.

```
marketing-analytics-ai/
├── data/mock/       → fake marketing data goes here
├── data/schemas/    → blueprints of what real API data looks like
├── src/             → all Python code lives here
├── prompts/         → instructions we give to the AI
├── notebooks/       → for exploration and experimentation
├── tests/           → for testing the code later
├── docs/            → extra documentation
```

**2. Initialized Git**
Git is version control — like "track changes" in Word but for code. Every time you finish something meaningful, you save a checkpoint. This means you can always go back if something breaks, and it lets you put the project on GitHub for your portfolio.

```bash
git init
git config --global init.defaultBranch main
git branch -m main
```

**3. Created a `.gitignore`**
Tells Git which files to never upload. Most importantly: your API keys (stored in `.env`) should never be public. This file prevents accidental leaks.

```
.env                  ← API keys — never upload this
__pycache__/          ← Python's temporary files, not needed
venv/                 ← your local environment, too large to share
```

**4. Created a virtual environment**
A virtual environment is an isolated Python workspace for this project. Dependencies installed here don't affect anything else on your system — and vice versa. Always activate it before working on the project.

```bash
# Install the required package first (Ubuntu-specific step)
sudo apt install python3.10-venv -y

# Create the virtual environment
python3 -m venv venv

# Activate it (do this every time you start a session)
source venv/bin/activate

# You'll know it's active when your prompt shows:
# (venv) avi-coding-pc@ubuntu:...
```

**5. Installed dependencies**
Four Python libraries this project needs:

| Library | What it does |
|---|---|
| `pandas` | Handles and analyzes data tables (like Excel, but in code) |
| `plotly` | Builds interactive charts and visualizations |
| `anthropic` | Official library to connect to Claude's AI API |
| `python-dotenv` | Loads API keys securely from a `.env` file |

```bash
pip install pandas plotly anthropic python-dotenv
pip freeze > requirements.txt
```

`requirements.txt` is a snapshot of everything installed. Anyone cloning the project runs `pip install -r requirements.txt` to get the exact same setup.

**6. Verified everything worked**
```bash
python3 -c "import pandas; import plotly; import anthropic; print('all good')"
# Output: all good ✅
```

---

#### What we learned
- Ubuntu requires `python3.10-venv` to be installed separately before you can create virtual environments
- Always activate venv before working: `source venv/bin/activate`
- `.gitignore` is a security essential, not optional
- `pip freeze > requirements.txt` should be run every time you install a new package

#### Prompts / questions that drove this step

These are the actual questions asked during this session that shaped what we built:

1. *"I want to document everything in an md file. Give me the best way to work with you so that I don't have to repeat things again and again."*
   → Led to creating `PROJECT_CONTEXT.md` as the single source of truth

2. *"Also give me the best ways to prompt so that AI yourself will understand my prompts for better results in an efficient way."*
   → Led to creating `AI_PROMPTING.md` with templates and best practices

3. *"Let's start with the first phase of this project."*
   → Led to breaking Phase 1 into 4 concrete steps with time estimates

4. *"Can you explain everything we just did in step one. Keep it brief and in plain English."*
   → Led to this DEVLOG format

5. *"I want to create documentation for the above — every time we finish a step, explain in plain English. Should we create a document for this and also have a section of what prompts led to each step?"*
   → Led to creating this DEVLOG.md file

---

#### Status after this session
- [x] Project folder created
- [x] Git initialized
- [x] Virtual environment working
- [x] Dependencies installed
- [x] PROJECT_CONTEXT.md created
- [x] AI_PROMPTING.md created
- [x] DEVLOG.md created
- [ ] Mock data schemas defined ← next
- [ ] Mock data generator written
- [ ] Basic data ingestion working
- [ ] First visualization working
- [ ] Claude API integrated

---

#### Next session starting point
```
Context: marketing-analytics-ai project, Phase 1
Last completed: Step 1 — project setup and environment
Next task: Step 2 — define mock data schemas for Meta, Google Ads, DV360, X Ads
Activate venv first: source venv/bin/activate
```

---

*— End of Session 1, Step 1 —*

---

<!-- Add new sessions above this line, newest at top -->
