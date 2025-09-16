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
You are an expert web crawler agent. Your task is to analyze the HTML of a webpage and determine the best course of action to achieve the user's objective.

**Objective:** {objective}
**Current URL:** {current_url}

**HTML Content:**
```html
{html_content}
```

**Instructions:**
Based on the HTML, decide on the next action. Your response **MUST** be a JSON object with an "action" and "args".

**Possible Actions & Arguments:**

1.  **`NAVIGATE_TO_LIST`**: The current page is a list of faculty members.
    *   `args`:
        *   `card_selector`: The CSS selector for the container of each professor/faculty member.
        *   `link_selector`: The CSS selector for the link to the professor's profile page, relative to the card.
        *   `name_selector`: The CSS selector for the professor's name, relative to the card.
        *   `title_selector`: The CSS selector for the professor's title or main role, relative to the card.
        *   `next_page_selector` (optional): The CSS selector for the "next page" button/link if there is one.

2.  **`EXTRACT_PROFILE`**: The current page is a detailed profile of a single faculty member.
    *   `args`: {{}} (no arguments needed)

3.  **`CLICK`**: You need to click a link or button to get closer to the faculty list.
    *   `args`:
        *   `selector`: The CSS selector for the element to click.
        *   `reason`: A brief explanation of why you are clicking this element.

4.  **`FINISH`**: The objective has been completed, or you are stuck.
    *   `args`:
        *   `reason`: A brief explanation of why you are finishing.

**Example Response for a list page:**
```json
{{
  "action": "NAVIGATE_TO_LIST",
  "args": {{
    "card_selector": ".faculty-card",
    "link_selector": "a.profile-link",
    "name_selector": "h2.name",
    "title_selector": "p.title",
    "next_page_selector": "a.next-page"
  }}
}}
```

**Example Response for a profile page:**
```
```
"""

OLLAMA_EXTRACTION_PROMPT = """
You are a machine that only returns JSON. Do not write any text, explanation, or conversational filler. Your entire response must be a single, valid JSON object.

Your task is to extract detailed information about a university professor from the provided HTML and complete the provided JSON object.

**Partially Scraped Data (complete this object):**
```json
{partial_data}
```

**Pydantic Model Schema (for reference):**
```python
class ProfessorProfile(BaseModel):
    name: str
    title: str
    email: Optional[str] = None
    profile_url: str
    research_interests: List[str] = Field(default_factory=list)
    publications: List[str] = Field(default_factory=list)
    lab: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
```

**Page Text Content of the Professor's Profile Page:**
```text
{page_text_content}
```

**Instructions:**
1.  Analyze the text to find the missing details for the professor.
2.  Complete the JSON object provided under "Partially Scraped Data".
3.  Extract research interests, publications, lab name, a description, and an image URL if available.
4.  Ensure your final output is ONLY the completed JSON object, conforming exactly to the schema. Do not include any other text.
"""