# NewsNinja – Your Personal AI Journalist

**Live App:** [https://newsninja-cs7cfjcqktgfp5urxavsbc.streamlit.app/](https://newsninja-cs7cfjcqktgfp5urxavsbc.streamlit.app/)

---

## Overview

**NewsNinja** is an AI-powered news intelligence application that acts as a personal journalist.
It collects recent news headlines and Reddit discussions on any topic, analyzes them using a high-performance Groq LLM, and generates a concise, neutral, broadcast-style summary.

The system is designed to be lightweight, fast, and deployable entirely on Streamlit Cloud.

---

## Key Features

* Topic-based news analysis
* Google News headline extraction
* Reddit discussion analysis
* AI-generated factual summaries using Groq LPU
* Streamlit Cloud deployment
* Modular backend architecture
* Ready for LangSmith observability

---

## Live Demo

Access the deployed application here:

**[https://newsninja-cs7cfjcqktgfp5urxavsbc.streamlit.app/](https://newsninja-cs7cfjcqktgfp5urxavsbc.streamlit.app/)**

---

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python
* BeautifulSoup
* Requests

### AI & LLM

* Groq LPU
* LLaMA 3.1 (8B Instant)

### Observability (Optional)

* LangSmith (LangChain tracing)

### Deployment

* Streamlit Cloud

---

## Project Structure

```
newsninja/
│
├── backend/
│   ├── __init__.py
│   ├── config.py
│   ├── news_scraper.py
│   ├── reddit_scraper.py
│   ├── summarizer.py
│   └── llm_groq.py
│
├── frontend/
│   └── app_frontend.py
│
├── requirements.txt
├── README.md
```

---

## How It Works

1. User enters a topic
2. Google News headlines are fetched
3. Reddit posts related to the topic are fetched
4. All content is passed to Groq LLM
5. A concise, factual summary is generated and displayed

---

## Environment Variables

The following secrets must be configured in **Streamlit Cloud → App Settings → Secrets**:

```toml
GROQ_API_KEY = "your_groq_key"

BRIGHTDATA_API_KEY = "your_brightdata_key"
BRIGHTDATA_ZONE = "web_unlocker"

LANGCHAIN_TRACING_V2 = true
LANGCHAIN_ENDPOINT = "https://api.smith.langchain.com"
LANGCHAIN_API_KEY = "your_langsmith_key"
LANGCHAIN_PROJECT = "NewsNinja"
```

---

## Local Development

### 1. Clone the repository

```bash
git clone https://github.com/Sachin432/newsninja.git
cd newsninja
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run frontend/app_frontend.py
```

---

## Known Limitations

* Google News scraping depends on public HTML structure
* Reddit API rate limits may apply
* Summaries are dependent on available source content
* Multilingual support is planned but not enabled yet

---

## Future Improvements

* Source transparency (show headlines used)
* Date filtering (last 24 hours / 7 days)
* Multi-source fusion (RSS + Reddit + News APIs)
* Confidence score for summaries
* Language detection (English / Hindi)
* User-selectable summary length

---

## Author

**Sachin Kumar**
M.Tech Data Science, DTU
