from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

# ── Read key from .env (local) OR st.secrets (Streamlit Cloud) ───────────────
def get_secret(key: str) -> str:
    # 1. Try environment variable (local .env via dotenv)
    value = os.getenv(key)
    if value:
        return value
    # 2. Try Streamlit secrets (Streamlit Cloud deployment)
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

groq_key = get_secret("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=groq_key,
)

# ── Writer ────────────────────────────────────────────────────────────────────
writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert research writer. Write clear, structured, and insightful reports.",
    ),
    (
        "human",
        """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual, and professional.
""",
    ),
])

writer_chain = writer_prompt | llm | StrOutputParser()

# ── Critic ────────────────────────────────────────────────────────────────────
critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a sharp and constructive research critic. Be honest and specific.",
    ),
    (
        "human",
        """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
...
""",
    ),
])

critic_chain = critic_prompt | llm | StrOutputParser()