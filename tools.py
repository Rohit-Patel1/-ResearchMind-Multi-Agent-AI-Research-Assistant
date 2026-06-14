from langchain.tools import tool
from tavily import TavilyClient
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import streamlit as st
import requests
import re
import os

load_dotenv()

# ── Read key from .env (local) OR st.secrets (Streamlit Cloud) ───────────────
def get_secret(key: str) -> str:
    value = os.getenv(key)
    if value:
        return value
    try:
        value = st.secrets.get(key)
        if value:
            return value
    except Exception:
        pass
    raise ValueError(
        f"{key} not found. "
        f"Add it to your .env file (local) or Streamlit Cloud secrets (deployed)."
    )

tavily = TavilyClient(api_key=get_secret("TAVILY_API_KEY"))

# ── URL blocklist ─────────────────────────────────────────────────────────────
SKIP_URL_PATTERNS = [
    r"\.pdf$",
    r"arxiv\.org/pdf/",
    r"arxiv\.org/e-print/",
    r"researchgate\.net/profile",
    r"academia\.edu",
    r"/download\?",
    r"\.doc$", r"\.docx$",
    r"\.ppt$", r"\.pptx$",
    r"\.zip$", r"\.gz$",
]

def _should_skip(url: str) -> bool:
    url_lower = url.lower()
    return any(re.search(p, url_lower) for p in SKIP_URL_PATTERNS)

def _is_binary_response(response) -> bool:
    content_type = response.headers.get("Content-Type", "").lower()
    if "pdf" in content_type or "octet-stream" in content_type:
        return True
    chunk = response.content[:512]
    if chunk.startswith(b"%PDF"):
        return True
    non_printable = sum(1 for b in chunk if b < 9 or (14 <= b < 32) or b > 126)
    if len(chunk) > 0 and non_printable / len(chunk) > 0.15:
        return True
    return False

def _redirect_arxiv(url: str) -> str:
    match = re.search(r"arxiv\.org/pdf/([^\s/]+)", url)
    if match:
        return f"https://arxiv.org/abs/{match.group(1)}"
    return url


@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information."""
    try:
        results = tavily.search(
            query=query,
            max_results=10,
            search_depth="advanced",
        )
        output = []
        for item in results["results"]:
            url = item["url"]
            if re.search(r"arxiv\.org/pdf/", url.lower()):
                url = _redirect_arxiv(url)
            output.append(
                f"Title: {item['title']}\n"
                f"URL: {url}\n"
                f"Snippet: {item['content'][:300]}"
            )
        return "\n\n-----\n\n".join(output)
    except Exception as e:
        return f"Search Error: {str(e)}"


@tool
def scrape_url(url: str) -> str:
    """Scrape webpage content from a URL. Skips PDFs and binary files."""
    if re.search(r"arxiv\.org/pdf/", url.lower()):
        url = _redirect_arxiv(url)
    if _should_skip(url):
        return f"[Skipped — binary or unsupported file type: {url}]"
    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            },
            stream=True,
        )
        response.raise_for_status()
        if _is_binary_response(response):
            return f"[Skipped — binary/PDF content detected at: {url}]"
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer",
                         "header", "aside", "form", "noscript"]):
            tag.decompose()
        main = (
            soup.find("article")
            or soup.find("main")
            or soup.find(id=re.compile(r"content|main|article", re.I))
            or soup.find(class_=re.compile(r"content|main|article|post|body", re.I))
            or soup.body
        )
        text = (main or soup).get_text(separator=" ", strip=True)
        text = re.sub(r"\s{3,}", "\n\n", text)
        return text[:5000] if text.strip() else f"[No readable content at: {url}]"
    except requests.exceptions.Timeout:
        return f"[Skipped — request timed out: {url}]"
    except requests.exceptions.HTTPError as e:
        return f"[Skipped — HTTP {e.response.status_code}: {url}]"
    except Exception as e:
        return f"[Scraping Error: {str(e)}]"