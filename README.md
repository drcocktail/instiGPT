# University Faculty Web Crawler

This project contains an intelligent web crawler designed to scrape faculty information from university websites.

## Setup

1.  **Install Dependencies:**
    Make sure you have Python 3 installed. Then, install the required packages using pip:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Set Up Environment Variables:**
    The crawler requires a Google Gemini API key. Create a file named `.env` in the root of the project directory and add your API key to it:
    ```
    GOOGLE_API_KEY=your_google_api_key_here
    ```

3.  **Run Ollama:**
    This project uses a local Ollama instance with the `llama3.2:latest` model for data extraction. Ensure your Ollama server is running before starting the crawler.

## How to Run

To start the crawler, run the `university_crawler.py` script from your terminal. You must provide a starting URL and a clear objective.

**Command:**
```bash
python university_crawler.py --url <STARTING_URL> --objective "<YOUR_OBJECTIVE>"
```

**Example:**
```bash
python university_crawler.py --url "https://engineering.wustl.edu/faculty/index.html" --objective "Scrape all faculty profiles from the Washington University in St. Louis engineering department"
```

The scraped data will be saved in the `scraped_data` directory.

