# 📊 Marketing Analytics AI

> A full-stack marketing analytics dashboard powered by Claude AI — built to demonstrate real-world data engineering, Python analysis, and LLM integration skills.

**[🚀 Live Demo](https://marketing-analytics-ai.streamlit.app)** · **[📓 Dev Log](DEVLOG.md)**

---

## What It Does

This project ingests mock marketing data from four ad platforms (Meta, Google Ads, DV360, X Ads), normalizes it into a unified dataset, runs statistical analysis, and surfaces AI-generated insights via Claude — all inside an interactive Streamlit dashboard.

| Feature | Details |
|---|---|
| 📥 Data ingestion | 4 platforms → normalized unified schema |
| 📈 Analysis | ROAS, CPC, CTR, weekly trends, conversion leaders |
| 🤖 AI insights | Claude generates plain-English summaries per analysis |
| 📊 Dashboard | Interactive Plotly charts + AI tab in Streamlit |
| ☁️ Deployed | Live on Streamlit Cloud |

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.4+-red?logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-6.0-blueviolet?logo=plotly)
![Claude](https://img.shields.io/badge/Claude-claude--sonnet--4-orange)
![Pandas](https://img.shields.io/badge/Pandas-2.0-150458?logo=pandas)

- **Claude API** (`anthropic` SDK) — AI-generated marketing insights
- **Streamlit** — dashboard UI and deployment
- **Plotly** — interactive charts
- **Pandas / NumPy** — data normalization and analysis
- **python-dotenv** — local secrets management

---

## Project Structure

```
marketing-analytics-ai/
├── src/
│   ├── dashboard.py      # Streamlit app — main entry point
│   ├── analyze.py        # Core analysis functions (ROAS, CTR, trends…)
│   ├── visualize.py      # Plotly chart generation
│   ├── ai_layer.py       # Claude API integration + mock mode
│   └── ingest.py         # Data normalization pipeline
├── data/
│   └── mock/
│       ├── unified.csv   # Normalized dataset (generated)
│       ├── meta.csv
│       ├── google_ads.csv
│       ├── dv360.csv
│       └── x_ads.csv
├── .streamlit/
│   └── config.toml       # Streamlit theme config
├── requirements.txt
├── DEVLOG.md             # Full session-by-session development log
└── README.md
```

---

## Architecture

```
Raw CSVs (4 platforms)
        │
        ▼
   ingest.py  ──►  data/mock/unified.csv
                          │
              ┌───────────┼────────────┐
              ▼           ▼            ▼
         analyze.py   visualize.py  ai_layer.py
              │           │            │
              └───────────┴────────────┘
                          │
                          ▼
                     dashboard.py
                    (Streamlit UI)
```

---

## Running Locally

### 1. Clone and install

```bash
git clone https://github.com/YOUR_USERNAME/marketing-analytics-ai.git
cd marketing-analytics-ai
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set up environment

```bash
cp .streamlit/secrets_template.toml .streamlit/secrets.toml
# Edit secrets.toml and add your Anthropic API key
```

Or create a `.env` file:
```
ANTHROPIC_API_KEY=your-key-here
```

### 3. Run the dashboard

```bash
streamlit run src/dashboard.py
```

Open http://localhost:8501

> **No API key?** The dashboard runs in mock mode by default (`USE_REAL_API = False` in `ai_layer.py`) — all charts and analysis work without any credentials.

---

## AI Mode

The AI insights tab uses Claude to generate plain-English summaries of the marketing data. Two modes:

| Mode | How to enable | Cost |
|---|---|---|
| **Mock** (default) | `USE_REAL_API = False` in `ai_layer.py` | Free |
| **Real AI** | `USE_REAL_API = True` + valid API key | ~$0.01–0.05 per run |

---

## Development Log

This project was built across 4 sessions. See [DEVLOG.md](DEVLOG.md) for the full breakdown of decisions, problems solved, and lessons learned.

| Session | What was built |
|---|---|
| 1 | Project setup, mock data schemas, data generator, normalization pipeline |
| 2 | `analyze.py`, `visualize.py`, `ai_layer.py` with mock mode + usage limits |
| 3 | Streamlit dashboard — overview, charts, AI insights tabs |
| 4 | GitHub push, Streamlit Cloud deployment, this README |

---

## License

MIT — free to use, fork, and build on.
