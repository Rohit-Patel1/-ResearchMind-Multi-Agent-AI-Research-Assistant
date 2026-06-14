from agents import writer_chain, critic_chain
from tools import web_search, scrape_url
import re


def extract_urls(text):
    return re.findall(r"https?://[^\s]+", text)


def run_research_pipeline(topic: str):

    state = {}

    
    print("\n" + "=" * 60)
    print("STEP 1 - WEB SEARCH")
    print("=" * 60)

    search_results = web_search.invoke({"query": topic})
    state["search_results"] = search_results
    print(search_results)

    
    print("\n" + "=" * 60)
    print("STEP 2 - URL EXTRACTION")
    print("=" * 60)

    urls = extract_urls(search_results)

    if not urls:
        print("No URLs found.")
        return

    print("Found URLs:")
    for i, url in enumerate(urls[:3], start=1):
        print(f"{i}. {url}")

    state["urls"] = urls[:3]

    
    print("\n" + "=" * 60)
    print("STEP 3 - SCRAPING CONTENT")
    print("=" * 60)

    scraped_content = []
    for url in urls[:3]:
        print(f"\nScraping: {url}")
        content = scrape_url.invoke({"url": url})
        scraped_content.append(f"\nSOURCE: {url}\n\n{content}")

    state["scraped_content"] = "\n\n".join(scraped_content)
    print("Scraping completed.")

    
    print("\n" + "=" * 60)
    print("STEP 4 - WRITING REPORT")
    print("=" * 60)

    research_data = (
        f"SEARCH RESULTS:\n{search_results}\n\n"
        f"SCRAPED CONTENT:\n{state['scraped_content']}"
    )

    report = writer_chain.invoke({
        "topic": topic,
        "research": research_data,
    })

    report += "\n\n## Sources\n"
    for url in urls[:3]:
        report += f"- {url}\n"

    state["report"] = report
    print(report)

    
    print("\n" + "=" * 60)
    print("STEP 5 - CRITIC REVIEW")
    print("=" * 60)

    feedback = critic_chain.invoke({"report": report})
    state["feedback"] = feedback
    print(feedback)

    return state


if __name__ == "__main__":
    topic = input("\nEnter research topic: ")
    run_research_pipeline(topic)