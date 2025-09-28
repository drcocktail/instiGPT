ANALYZE_PAGE_PROMPT = """
You are a web scraper agent. Your task is to analyze the provided clean HTML and identify all interactive elements like links (<a>), buttons (<button>), and form inputs (<input>, <select>, <textarea>).
For each element, provide its text, a unique ID, and a robust CSS selector.
Return a JSON object with two keys:
1. "page_summary": A brief, one-sentence summary of the page's purpose.
2. "interactive_elements": A list of all identified interactive elements. Each element in the list should be a JSON object with the following keys: "id", "tag", "text", and "selector".

Here is the clean HTML:
{html}
"""

DEVISE_STRATEGY_PROMPT = """
You are a master web scraping strategist. Your goal is to create a complete, step-by-step plan to achieve the user's objective.
The plan should be returned as a single JSON object that can be parsed into a `ScrapingPlan` model.

**Objective:**
{objective}

**Page Context:**
This is the context from the starting URL. It includes a page summary and a list of interactive elements with their CSS selectors.
{context}

**Instructions:**
1.  Analyze the objective and the page context.
2.  Identify the repeating element that represents a single item to be scraped (e.g., a faculty member's card in a directory).
3.  Devise a series of steps to be performed on each of these items. This will form a loop.
4.  The steps inside the loop should typically include:
    a. Clicking a link to go to a detail page.
    b. Extracting the required information on the detail page.
    c. Navigating back to the main directory page to process the next item.
5.  If there is pagination, identify the selector for the "next page" button.
6.  Construct a final plan as a JSON object.

**Output Format:**
The output must be a JSON object with a "steps" key, which is a list of plan steps.
**Crucially, the `action` for each step MUST be one of the following literal strings: 'goto', 'click', 'type', 'extract_details', 'loop', 'go_back'. Do not invent new actions.**
Use the 'loop' action for iterating over faculty cards.
Inside the loop, define the steps to get to the detail page, extract data, and go back.

Example of a good plan:
```json
{{
  "steps": [
    {{
      "action": "loop",
      "selector": "div.faculty-card-class",
      "steps": [
        {{
          "action": "click",
          "selector": "a.profile-link-class"
        }},
        {{
          "action": "extract_details",
          "model_definition": {{
            "name": "h1.faculty-name",
            "title": "p.faculty-title",
            "email": "a.faculty-email"
          }}
        }},
        {{
          "action": "go_back"
        }}
      ]
    }}
  ]
}}
```

Now, create the plan for the given objective and context.
"""

GEMINI_ANALYSIS_PROMPT = """
You are a web scraping strategist. You are helping to crawl a university website to extract faculty information.

**Current Objective:** {objective}
**Current URL:** {current_url}

Analyze the following HTML content and determine the best next action. You should return a JSON object with:
- "action": One of ["CLICK", "NAVIGATE", "EXTRACT_LIST", "EXTRACT_PROFILE", "FINISH"]
- "selector": CSS selector for the element to interact with (if action is CLICK)
- "url": URL to navigate to (if action is NAVIGATE) 
- "reason": Brief explanation of why this action was chosen
- "faculty_found": Boolean indicating if faculty profiles are visible on this page

Actions explained:
- CLICK: Click on a link or button (provide CSS selector)
- NAVIGATE: Go to a specific URL (provide the URL)
- EXTRACT_LIST: Extract faculty data from a directory/list page (when multiple faculty profiles are visible)
- EXTRACT_PROFILE: Extract faculty data from a single faculty member's profile page
- FINISH: End crawling (when no more useful actions can be taken)

**Instructions:**
Based on the HTML, decide on the next action. Your response **MUST** be a JSON object with an "action" and "args". The "action" key **MUST** be one of the following strings: 'NAVIGATE_TO_LIST', 'EXTRACT_PROFILE', 'CLICK', or 'FINISH'.

**Possible Actions & Arguments:**

1.  **`NAVIGATE_TO_LIST`**: The current page is a list of faculty members.

HTML Content:
{html_content}
"""

GEMINI_CORRECTION_PROMPT = """
You are an expert web crawler agent. Your previous attempt to create an action plan was invalid. You must analyze your mistake and provide a corrected, valid JSON action plan.

**Objective:** {objective}
**Current URL:** {current_url}

**Your Previous Invalid Plan:**
```json
{invalid_plan}
```

**Reason it was Invalid:**
{failure_reason}

**Instructions:**
1.  Review the reason your last plan failed.
2.  Re-analyze the HTML content below.
3.  Provide a new, valid JSON response that corrects the mistake.
4.  The "action" key **MUST** be one of: 'NAVIGATE_TO_LIST', 'EXTRACT_PROFILE', 'CLICK', or 'FINISH'.
5.  All actions **MUST** include all of their required arguments. For example, 'CLICK' requires a 'selector'.

**HTML Content:**
```html
{html_content}
```

**Provide a new, valid JSON object.**
"""

OLLAMA_EXTRACTION_PROMPT = """
You are a machine that only returns JSON. Do not write any text, explanation, or conversational filler. Your entire response must be a single, valid JSON object.

Extract the following information for each faculty member found:
- name: Full name
- title: Job title or position
- email: Email address if available
- department: Department or school
- research_interests: List of research areas/interests
- profile_url: Link to detailed profile if available
- image_url: Profile photo URL if available
- phone: Phone number if available
- office: Office location if available

Return a JSON array of faculty objects. If no faculty information is found, return an empty array.

**Page Text Content of the Professor's Profile Page:**
```text
{page_text_content}
```

**Instructions:**
1.  Analyze the text to find the missing details for the professor.
"""
