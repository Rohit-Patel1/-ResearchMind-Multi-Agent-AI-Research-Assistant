# 🔬 ResearchMind — Multi-Agent AI Research Assistant

![ResearchMind Banner](https://img.shields.io/badge/ResearchMind-AI%20Research%20Agent-ff8c32?style=for-the-badge&logo=robot&logoColor=white)

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.3+-1C3C3C?style=flat-square&logo=chainlink&logoColor=white)](https://langchain.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA%203.3-F55036?style=flat-square&logo=groq&logoColor=white)](https://groq.com)
[![Tavily](https://img.shields.io/badge/Tavily-Search%20API-0EA5E9?style=flat-square)](https://tavily.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

**A production-grade multi-agent AI system that autonomously searches the web, scrapes sources, writes structured research reports, and critiques its own output — all in real time.**

[Live Demo](#) · [Report Bug](https://github.com/YOUR_USERNAME/researchmind/issues) · [Request Feature](https://github.com/YOUR_USERNAME/researchmind/issues)

</div>

---

## 📸 Screenshots

| Main Interface | Research Dashboard |
|---|---|
| ![Main](https://via.placeholder.com/500x300/0a0a0f/ff8c32?text=ResearchMind+UI) | ![Dashboard](https://via.placeholder.com/500x300/0a0a0f/50c878?text=Research+Dashboard) |

---

## 🧠 What Is ResearchMind?

ResearchMind is a **multi-agent AI research pipeline** built with LangChain, Groq (LLaMA 3.3 70B), and Tavily Search. You type a research topic — four specialized AI agents collaborate to deliver a polished, structured report in under 60 seconds.

### How It Works

```
User Input
    │
    ▼
┌─────────────────┐
│  Search Agent   │  ← Tavily API: finds 10 relevant sources
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Reader Agent   │  ← Scrapes & extracts content from top URLs
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Writer Chain   │  ← LLaMA 3.3 70B drafts a structured report
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Critic Chain   │  ← Reviews, scores (X/10), gives feedback
└─────────────────┘
         │
         ▼
    Final Report
  (Download as MD / PDF / DOCX)
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **Multi-Agent Pipeline** | 4 specialized agents: Search → Read → Write → Critique |
| 📊 **Research Dashboard** | Live metrics — sources found, words written, quality score |
| 🗂 **Tabbed Results** | Report / Sources / Analysis / Critic / Raw Data |
| 📈 **Interactive Charts** | Source distribution pie, keyword frequency bar, sentiment analysis |
| 🔗 **Source Cards** | Domain, type badge, credibility rating, direct link |
| ⬇ **Export Options** | Download as Markdown, PDF, or DOCX |
| 📋 **Search History** | Sidebar stores last 12 reports — reload any with one click |
| ⚙ **Configurable** | Adjust max sources (1–5) and report depth |
| 🛡 **PDF Guard** | Auto-skips binary PDFs and paywalled sources |
| 🎨 **Dark UI** | Custom glassmorphism theme with orange accent |

---

## 🏗 Architecture

```
researchmind/
├── app.py              # Streamlit UI — main entry point
├── agents.py           # Writer & Critic LangChain chains (Groq / LLaMA 3.3)
├── tools.py            # Web search (Tavily) + URL scraper (BeautifulSoup)
├── pipeline.py         # CLI version of the pipeline (for testing)
├── report_exporter.py  # PDF (ReportLab) + DOCX (python-docx) export
├── requirements.txt    # All dependencies
└── .env                # API keys (never commit this)
```

### Tech Stack

| Layer | Technology |
|---|---|
| **UI** | Streamlit 1.35+ |
| **LLM** | Groq API → LLaMA 3.3 70B Versatile |
| **Orchestration** | LangChain 0.3 (chains, prompts, parsers) |
| **Search** | Tavily Search API (advanced depth, 10 results) |
| **Scraping** | Requests + BeautifulSoup4 |
| **Visualization** | Plotly (graph_objects only — no pandas dependency) |
| **Export** | ReportLab (PDF) + python-docx (DOCX) |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- A [Groq API key](https://console.groq.com) (free)
- A [Tavily API key](https://tavily.com) (free tier available)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/researchmind.git
cd researchmind
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and add your keys:

```env
TAVILY_API_KEY="tvly-dev-your_key_here"
GROQ_API_KEY="gsk_your_key_here"
```

### 5. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🔑 Getting API Keys

### Groq API Key (Free)
1. Go to [console.groq.com](https://console.groq.com)
2. Sign up → API Keys → Create New Key
3. Copy and paste into `.env`

### Tavily API Key (Free Tier)
1. Go to [tavily.com](https://tavily.com)
2. Sign up → Dashboard → API Keys
3. Copy and paste into `.env`

---

## 📦 Installation Details

```
requirements.txt includes:

LangChain Ecosystem    → langchain, langchain-core, langchain-groq
Search                 → tavily-python
Scraping               → beautifulsoup4, requests, lxml
Environment            → python-dotenv
Visualization          → plotly
PDF Export             → reportlab
DOCX Export            → python-docx
UI                     → streamlit
```

---

## 🖥 Usage

### Web UI (Recommended)

1. Enter a research topic in the input field
2. Click **⚡ Run Research Pipeline**
3. Watch the 4-step pipeline execute in real time
4. View results across 5 tabs: Report, Sources, Analysis, Critic, Raw Data
5. Export as Markdown / PDF / DOCX

### CLI (Terminal)

```bash
python pipeline.py
# Enter research topic when prompted
```

### Sidebar Features

- **Settings** — adjust max sources (1–5) and report depth
- **Recent Reports** — click "↩ Load" to instantly reload any previous report
- Toggle sidebar open/closed using the `❯` / `❮` arrow on the left edge

---

## 🛡 Built-in Safety Features

ResearchMind automatically handles problematic URLs:

| Scenario | Behavior |
|---|---|
| Direct PDF link (e.g. arxiv.org/pdf/...) | Redirected to HTML abstract page |
| Binary content detected | Skipped with clean message |
| Paywalled sites (ResearchGate, Academia.edu) | Skipped automatically |
| HTTP timeout | Graceful skip, continues pipeline |
| Rate limit errors | Returns descriptive error, pipeline continues |

---

## 📊 Example Output

**Topic:** *"Small Language Models and Agentic AI"*

```
Sources Found:    10
Sources Scraped:   3
Report Words:    574
Quality Score:   8/10

Report sections:
  • Introduction
  • Key Finding 1 — SLMs vs LLMs for agentic tasks
  • Key Finding 2 — Economic advantages (10–30× cheaper)
  • Key Finding 3 — Modular heterogeneous architectures
  • Conclusion
  • Sources (with URLs)

Critic Feedback:
  Score: 8/10
  Strengths: Well-structured, factual, cites real papers
  Areas to Improve: Could include more empirical benchmarks
  Verdict: Solid research report with actionable insights
```

---

## 🚢 Deployment

### Streamlit Community Cloud (Free — Recommended)

1. Push your code to GitHub (make sure `.env` is in `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set secrets in **Advanced Settings**:
   ```
   TAVILY_API_KEY = "tvly-dev-your_key"
   GROQ_API_KEY   = "gsk_your_key"
   ```
5. Click **Deploy** — you get a public URL instantly

### Railway / Render

Set environment variables in the dashboard and use:
```
Start command: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

---

## 🔧 Configuration

| Setting | Default | Description |
|---|---|---|
| `max_sources` | 3 | Number of URLs to scrape (1–5) |
| `report_depth` | Standard | Standard / Deep / Quick Summary |
| `model` | llama-3.3-70b-versatile | Groq model for writer & critic |
| `temperature` | 0 | LLM temperature (0 = deterministic) |
| `max_results` | 10 | Number of Tavily search results |

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

### Ideas for Contributions

- [ ] Add memory across sessions (SQLite / Redis)
- [ ] Support for additional LLM providers (OpenAI, Anthropic)
- [ ] PDF ingestion as a research source
- [ ] Multi-language report generation
- [ ] Scheduled research reports via cron
- [ ] REST API endpoint for programmatic access

---

## 📝 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Rohit Patel**

- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/YOUR_PROFILE)

---

## 🙏 Acknowledgements

- [LangChain](https://langchain.com) — for the agent orchestration framework
- [Groq](https://groq.com) — for blazing-fast LLaMA 3.3 inference
- [Tavily](https://tavily.com) — for the research-grade search API
- [Streamlit](https://streamlit.io) — for the rapid UI framework

---

<div align="center">

**If this project helped you, please give it a ⭐ on GitHub!**

Made with ❤️ by Rohit Patel

</div>
