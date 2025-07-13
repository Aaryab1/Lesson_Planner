from typing import override, List, Optional
from pydantic import BaseModel, Field
import requests
from dotenv import load_dotenv
import os
import asyncio
import time
import logging
from urllib.parse import urljoin, urlparse
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
load_dotenv(override = "True")
google_search_api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
cse_id = os.getenv("CSE_ID")
def search_google_cse(query, api_key, cse_id, num_results=15):
    """Search Google Custom Search with better error handling"""
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cse_id,
        "q": query,
        "num": num_results
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        results = response.json().get("items", [])
        links = [item["link"] for item in results]
        print(f"Found {len(links)} search results")
        return links
    except requests.exceptions.RequestException as e:
        print(f"Error in Google search: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error in search: {e}")
        return []

def filter_links(links):
    """Filter out unwanted domains and invalid URLs"""
    blacklist = ["youtube", "udemy", "coursera", "pinterest", "linkedin", "facebook", "twitter", "instagram"]
    filtered = []
    
    for link in links:
        try:
            # Parse URL to check if it's valid
            parsed = urlparse(link)
            if not parsed.scheme or not parsed.netloc:
                continue
                
            # Check blacklist
            if any(b in link.lower() for b in blacklist):
                continue
                
            # Prefer educational and reliable sources
            if any(domain in link.lower() for domain in ['edu', 'britannica', 'nationalgeographic', 'smithsonian']):
                filtered.insert(0, link)  # Prioritize these
            else:
                filtered.append(link)
                
        except Exception:
            continue
            
    print(f"Filtered to {len(filtered)} valid links")
    return filtered


from newspaper import Article

# Define data models
class SourceInfo(BaseModel):
    url: str = Field(description="The URL of the source website.")
    content_fetched: bool = Field(description="Whether content was successfully fetched from this source.")
    content: str = Field(description="The extracted content from the source, if available.")

class ScrapeOutput(BaseModel):
    topic: str = Field(description="The topic that was scraped.")
    summary: str = Field(description="A summary of the scraped content.")
    sources: List[SourceInfo] = Field(description="A list of source information objects for each website scraped.")

def extract_text_from_url(url, timeout=15):
    """Extract text with better error handling and retry logic"""
    try:
        # Set user agent to avoid blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Create article with proper configuration
        article = Article(url)
        article.config.request_timeout = timeout
        article.config.browser_user_agent = headers['User-Agent']
        article.config.fetch_images = False
        article.config.memoize_articles = False
        
        # Download and parse
        article.download()
        article.parse()
        
        # Additional validation
        if len(article.text.strip()) < 100:
            print(f"Content too short from {url}: {len(article.text)} chars")
            return ""
            
        print(f"Successfully extracted {len(article.text)} characters from {url}")
        return article.text.strip()
        
    except Exception as e:
        print(f"Error extracting from {url}: {e}")
        # Fallback: try basic requests + BeautifulSoup
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            if len(text.strip()) < 100:
                print(f"Fallback content too short from {url}: {len(text)} chars")
                return ""
                
            print(f"Fallback extraction successful: {len(text)} characters from {url}")
            return text.strip()
            
        except Exception as fallback_error:
            print(f"Fallback extraction also failed for {url}: {fallback_error}")
            return ""


def scrape_topic_content(topic, api_key, cse_id, min_content_length=200, max_sources=10):
    """Enhanced scraping with better content aggregation and source tracking"""
    print(f"🔍 Searching content for: {topic}")
    
    # Try multiple search variations for better results
    search_queries = [
        topic,
        f"{topic} explanation",
        f"{topic} educational content"
    ]
    
    all_links = []
    for query in search_queries:
        links = search_google_cse(query, api_key, cse_id, num_results=8)
        all_links.extend(links)
    
    # Remove duplicates while preserving order
    unique_links = list(dict.fromkeys(all_links))
    filtered_links = filter_links(unique_links)
    
    print(f"Processing {len(filtered_links)} unique links...")
    
    sources = []
    successful_extractions = 0
    total_content_length = 0
    
    for i, link in enumerate(filtered_links[:max_sources]):
        print(f"Processing {i+1}/{min(len(filtered_links), max_sources)}: {link}")
        
        content = extract_text_from_url(link)
        content_fetched = len(content) >= min_content_length
        
        source_info = SourceInfo(
            url=link,
            content_fetched=content_fetched,
            content=content if content_fetched else ""
        )
        sources.append(source_info)
        
        if content_fetched:
            successful_extractions += 1
            total_content_length += len(content)
        
        # Add small delay to be respectful
        time.sleep(0.5)
    
    print(f"✅ Successfully extracted content from {successful_extractions}/{len(sources)} sources")
    print(f"📊 Total content: {total_content_length} characters")
    
    # Create comprehensive summary
    if successful_extractions > 0:
        all_content = "\n\n".join([s.content for s in sources if s.content_fetched])
        summary = f"Successfully gathered content about '{topic}' from {successful_extractions} sources. "
        summary += f"Total content length: {total_content_length} characters."
    else:
        all_content = ""
        summary = f"Could not extract sufficient content about '{topic}' from the available sources. "
        summary += "This might be due to website restrictions or content format issues."
    
    return ScrapeOutput(
        topic=topic,
        summary=summary,
        sources=sources
    )


from agents import Agent, Runner, trace, function_tool, handoff

class LessonTopic(BaseModel):
    title: str = Field(description="Sub-topic title")
    duration_minutes: int = Field(description="Time required to cover this sub-topic")
    description: str = Field(description="Short overview of this topic")

class LessonPlan(BaseModel):
    topic: str
    grade_level: str
    duration_minutes: int
    learning_objectives: List[str]
    materials_needed: List[str]
    lesson_overview: List[LessonTopic]
    exercises: List[str]
    assessment: List[str]
    urls: List[str]

lesson_planner_agent = Agent(
    name="Lesson Planner",
    instructions="""
You are an expert education assistant. You will be given a topic summary and multiple pieces of scraped content from different websites.

Your job is to create a complete lesson plan using that content. Follow this exact structure:

- topic: The name of the topic.
- grade_level: The intended grade level (extract or guess from context).
- duration_minutes: Estimated total time required to complete the lesson.
- learning_objectives: 3–5 objectives that students should achieve.
- materials_needed: List of materials needed to teach the topic.
- lesson_overview: A list of subtopics, each with:
    - title
    - duration_minutes
    - description
- exercises: 2–4 classroom exercises.
- assessment: 2–4 questions to assess student understanding.
- urls: All source URLs used (from the provided content).

Use only the given summary and source content to generate your answer. Keep output clean and structured.

Ensure your output strictly matches the expected fields.
""",
    model="gpt-4o-mini",
    output_type=LessonPlan,
)

@function_tool
def scrape_tool(topic: str) -> ScrapeOutput:
    """Enhanced scraping tool that returns structured output"""
    return scrape_topic_content(topic, google_search_api_key, cse_id)







instructions_for_scrapper = """
Use the scrape_web tool to fetch the most relevant, readable content for a given topic.

After successfully gathering content, you can hand off to the Lesson Planner agent to create a comprehensive lesson plan using the scraped content.

Return a structured output in the following format:
- topic: the original topic
- summary: a clean, concise paragraph combining the main points from all sources
- sources: a list of websites searched, indicating whether content was fetched or not. For each source, include:
    - url
    - content_fetched (true/false)
    - content (actual extracted text, or a short explanation why not)

You must include all websites you attempted to fetch from, whether successful or not.

Once content is gathered, you can transfer to the Lesson Planner agent to create a lesson plan from the scraped content.
"""



scraper_agent = Agent(
    name="Content Fetcher",
    instructions=instructions_for_scrapper,
    tools=[scrape_tool],
    handoffs=[lesson_planner_agent],
    output_type=ScrapeOutput,  # This enables validation + parsing
)

with trace("scrape_tool"):
    content = Runner.run_sync(scraper_agent, "Simple Machines for grade 6 science")
    print(content)
    
