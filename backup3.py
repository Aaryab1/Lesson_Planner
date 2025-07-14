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
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
load_dotenv(override = "True")
google_search_api_key = os.getenv("GOOGLE_SEARCH_API_KEY")
cse_id = os.getenv("CSE_ID")

# Initialize FastAPI app
app = FastAPI(
    title="Lesson Planner Bot API",
    description="An AI-powered lesson planning assistant that scrapes educational content and creates comprehensive lesson plans",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


def scrape_topic_content(queries, api_key, cse_id, min_content_length=200, max_sources=5, max_content_per_source=2000, min_successful_sources=2, min_total_content=1000, max_rounds=3):
    """Enhanced scraping with dynamic search depth. Accepts a list of queries and will try up to max_rounds if results are insufficient."""
    if isinstance(queries, str):
        queries = [queries]
    all_links = []
    all_sources = []
    successful_extractions = 0
    total_content_length = 0
    round_num = 0
    used_queries = set()
    while round_num < max_rounds:
        print(f"🔍 [Round {round_num+1}] Searching content for queries: {queries}")
        round_links = []
        for query in queries:
            if query in used_queries:
                continue
            search_queries = [query]
            for q in search_queries:
                links = search_google_cse(q, api_key, cse_id, num_results=5)
                round_links.extend(links)
            used_queries.add(query)
        # Remove duplicates while preserving order
        unique_links = list(dict.fromkeys(all_links + round_links))
        filtered_links = filter_links(unique_links)
        print(f"Processing {len(filtered_links)} unique links...")
        sources = []
        round_successful = 0
        round_content_length = 0
        for i, link in enumerate(filtered_links[:max_sources]):
            print(f"Processing {i+1}/{min(len(filtered_links), max_sources)}: {link}")
            content = extract_text_from_url(link)
            if len(content) > max_content_per_source:
                content = content[:max_content_per_source] + "... [content truncated]"
                print(f"Content truncated to {max_content_per_source} characters")
            content_fetched = len(content) >= min_content_length
            source_info = SourceInfo(
                url=link,
                content_fetched=content_fetched,
                content=content if content_fetched else ""
            )
            sources.append(source_info)
            if content_fetched:
                round_successful += 1
                round_content_length += len(content)
            time.sleep(0.5)
        all_links = unique_links
        all_sources.extend(sources)
        successful_extractions += round_successful
        total_content_length += round_content_length
        print(f"✅ [Round {round_num+1}] Extracted from {round_successful}/{len(sources)} sources, {round_content_length} chars")
        # Check if we have enough good content
        if successful_extractions >= min_successful_sources and total_content_length >= min_total_content:
            break
        # Otherwise, ask the agent to generate new queries (broader/narrower/reworded)
        round_num += 1
        if round_num < max_rounds:
            print(f"⚠️ Not enough content, should try new queries in next round.")
            # Instruct the agent to generate new queries in the next round (handled by agent instructions)
            # For now, just try some generic fallbacks if agent doesn't provide new queries
            queries = [q + " educational resources" for q in queries]
    print(f"📊 Total successful sources: {successful_extractions}, total content: {total_content_length} characters")
    if successful_extractions > 0:
        max_total_content = 8000
        all_content_parts = [s.content for s in all_sources if s.content_fetched]
        if total_content_length > max_total_content:
            print(f"⚠️ Total content too long ({total_content_length} chars), truncating to {max_total_content}")
            truncated_content = ""
            for content_part in all_content_parts:
                if len(truncated_content) + len(content_part) < max_total_content:
                    truncated_content += content_part + "\n\n"
                else:
                    break
            all_content = truncated_content
        else:
            all_content = "\n\n".join(all_content_parts)
        summary = f"Successfully gathered content from {successful_extractions} sources. Total content length: {len(all_content)} characters."
    else:
        all_content = ""
        summary = "Could not extract sufficient content from the available sources. This might be due to website restrictions or content format issues."
    return ScrapeOutput(
        topic=queries[0] if queries else "",
        summary=summary,
        sources=all_sources
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

# Step 1: Update the scraper agent's instructions for dynamic search depth
instructions_for_scrapper = """
You are an expert at finding educational content for lesson planning.

1. When given a user query (e.g., 'photosynthesis for grade 6'), rewrite it into 2–3 Google search queries that will find the most relevant educational resources, lesson plans, activities, and explanations for teachers and students.
   - Example rewrites: 
     - 'photosynthesis lesson plan for grade 6'
     - 'photosynthesis activities for middle school'
     - 'photosynthesis explained for 6th grade students'

2. Use the scrape_web tool with each of these queries to gather content.

3. If the first set of queries yields insufficient or low-quality results (e.g., less than 2 good sources or less than 1000 characters of content), generate and try additional queries (broader, narrower, or reworded). Repeat up to 3 rounds if needed.

4. Aggregate the results, remove duplicates, and return a structured output:
   - topic: the original topic
   - summary: a clean, concise paragraph combining the main points from all sources
   - sources: a list of websites searched, indicating whether content was fetched or not. For each source, include:
       - url
       - content_fetched (true/false)
       - content (actual extracted text, or a short explanation why not)
"""

# Step 2: Update the scraping logic to allow for multiple rounds

# Update the scrape_tool to accept a list of queries
@function_tool
def scrape_tool(queries: list[str]) -> ScrapeOutput:
    """Enhanced scraping tool that returns structured output for a list of queries"""
    return scrape_topic_content(queries, google_search_api_key, cse_id)

# Update scraper_agent to use new instructions (already done above)
scraper_agent = Agent(
    name="Content Fetcher",
    instructions=instructions_for_scrapper,
    tools=[scrape_tool],
    handoffs=[lesson_planner_agent],
    output_type=ScrapeOutput,  # This enables validation + parsing
)

# 1. Define the Validation Agent
validation_agent_instructions = """
You are an input validation assistant for an educational lesson planning tool.
Your job is to determine if a user query is a valid educational topic or question.

- If the query is clearly educational (e.g., a school subject, concept, or topic), respond with:
  VALID: <repeat the query>
- If the query is not educational, inappropriate, or irrelevant, respond with:
  INVALID: <short reason why>

Only allow queries that are suitable for generating lesson plans for students or teachers.
"""

validation_agent = Agent(
    name="Validation Agent",
    instructions=validation_agent_instructions,
    model="gpt-4o-mini",
    output_type=str,
)

# with trace("scrape_tool"):
#     content = Runner.run_sync(scraper_agent, "Simple Machines for grade 6 science")
#     print(content)

# FastAPI Request/Response Models
class LessonPlanRequest(BaseModel):
    topic: str = Field(description="The educational topic to create a lesson plan for")
    grade_level: Optional[str] = Field(default=None, description="Optional grade level specification")

class LessonPlanResponse(BaseModel):
    success: bool
    lesson_plan: Optional[LessonPlan] = None
    error: Optional[str] = None
    message: str

# FastAPI Endpoints
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Lesson Planner Bot API",
        "version": "1.0.0",
        "endpoints": {
            "POST /create-lesson-plan": "Create a lesson plan for a given topic",
            "GET /health": "Health check endpoint"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Lesson Planner Bot is running"}

@app.post("/create-lesson-plan", response_model=LessonPlanResponse)
async def create_lesson_plan(request: LessonPlanRequest):
    """
    Create a comprehensive lesson plan for the given topic.
    This endpoint will:
    1. Validate the query is educational
    2. Scrape educational content from the web
    3. Generate a structured lesson plan
    4. Return the complete lesson plan with all components
    """
    try:
        # Prepare the query
        query = request.topic
        if request.grade_level:
            query = f"{request.topic} for {request.grade_level}"
        print(f"🎯 Processing lesson plan request: {query}")

        # 2. Validate the query using the validation agent
        validation_result = await Runner.run(validation_agent, query)
        print(f"🛡️ Validation agent result: {validation_result}")
        print(f"Validation agent raw result: {validation_result} (type: {type(validation_result)})")
        # Robust extraction of string output
        if not isinstance(validation_result, str):
            # Try to extract string from known attributes
            if hasattr(validation_result, 'output') and isinstance(validation_result.output, str):
                validation_result = validation_result.output
                print(f"Extracted string from .output: {validation_result}")
            elif hasattr(validation_result, 'final_output') and isinstance(validation_result.final_output, str):
                validation_result = validation_result.final_output
                print(f"Extracted string from .final_output: {validation_result}")
            else:
                return LessonPlanResponse(
                    success=False,
                    error="Validation agent did not return a string response.",
                    message="Could not validate query."
                )
        if validation_result.strip().startswith("INVALID:"):
            return LessonPlanResponse(
                success=False,
                error=validation_result.strip(),
                message="Query is not educational."
            )
        if not validation_result.strip().startswith("VALID:"):
            return LessonPlanResponse(
                success=False,
                error="Validation agent returned an unexpected response.",
                message="Could not validate query."
            )
        # Extract the cleaned query after 'VALID:'
        query = validation_result.strip()[len("VALID:"):].strip()

        # 3. Run the scraper agent with the query using async runner
        run_result = await Runner.run(scraper_agent, query)
        
        # Debug: print the structure of run_result
        print(f"🔍 Scraper run_result type: {type(run_result)}")
        print(f"🔍 Scraper run_result attributes: {dir(run_result)}")
        
        # Extract the actual result from the RunResult
        if hasattr(run_result, 'final_output') and run_result.final_output:
            result = run_result.final_output
            print(f"✅ Using run_result.final_output: {type(result)}")
        elif hasattr(run_result, 'output') and run_result.output:
            result = run_result.output
            print(f"✅ Using run_result.output: {type(result)}")
        else:
            # Fallback: try to get the result directly
            result = run_result
            print(f"⚠️ Using run_result directly: {type(result)}")
        
        # If we got a ScrapeOutput, we need to hand off to the lesson planner
        if isinstance(result, ScrapeOutput):
            print(f"📚 Content scraped successfully, creating lesson plan...")
            
            # Create a concise prompt for the lesson planner to avoid context overflow
            successful_sources = [s for s in result.sources if s.content_fetched]
            source_urls = [s.url for s in successful_sources[:3]]  # Limit to first 3 sources
            
            # Create a more concise prompt
            prompt = f"""Create a lesson plan for: {request.topic}

Summary: {result.summary}

Key information from sources:
"""
            
            # Add key content from first few sources (truncated)
            for i, source in enumerate(successful_sources[:2]):  # Only first 2 sources
                truncated_content = source.content[:1000] + "..." if len(source.content) > 1000 else source.content
                prompt += f"\nSource {i+1}: {truncated_content}\n"
            
            prompt += f"\nSource URLs: {', '.join(source_urls)}"
            
            # Hand off to lesson planner agent using async runner
            run_result = await Runner.run(lesson_planner_agent, prompt)
            
            # Debug: print the structure of lesson planner run_result
            print(f"🔍 Lesson planner run_result type: {type(run_result)}")
            print(f"🔍 Lesson planner run_result attributes: {dir(run_result)}")
            
            # Extract the actual lesson plan from the RunResult
            if hasattr(run_result, 'final_output') and run_result.final_output:
                lesson_plan = run_result.final_output
                print(f"✅ Using run_result.final_output for lesson plan: {type(lesson_plan)}")
            elif hasattr(run_result, 'output') and run_result.output:
                lesson_plan = run_result.output
                print(f"✅ Using run_result.output for lesson plan: {type(lesson_plan)}")
            else:
                # Fallback: try to get the result directly
                lesson_plan = run_result
                print(f"⚠️ Using run_result directly for lesson plan: {type(lesson_plan)}")
            
            return LessonPlanResponse(
                success=True,
                lesson_plan=lesson_plan,
                message=f"Successfully created lesson plan for '{request.topic}'"
            )
        else:
            # If we got a LessonPlan directly (handoff worked)
            return LessonPlanResponse(
                success=True,
                lesson_plan=result,
                message=f"Successfully created lesson plan for '{request.topic}'"
            )
            
    except Exception as e:
        print(f"❌ Error creating lesson plan: {str(e)}")
        return LessonPlanResponse(
            success=False,
            error=str(e),
            message=f"Failed to create lesson plan for '{request.topic}'"
        )

# Run the FastAPI server
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
    
