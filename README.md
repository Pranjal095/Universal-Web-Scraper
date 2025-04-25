# Universal Web Scraper Tool

A Streamlit‑based application to scrape one or more websites, parse and index their content, and interactively query the data using a local LLM (Llama 3.1 via Ollama).

## Features

- Multi‐URL support: input multiple URLs (one per line)  
- Cloudflare bypass using headless Chromium (`DrissionPage`)  
- HTML parsing & content grouping (`BeautifulSoup`)  
- Clean text extraction & heading‑based grouping  
- Embeddings generation (`sentence-transformers`)  
- FAISS L2 indexing of content for fast retrieval  
- LLM‑powered querying with subquery decomposition  
- JSON export of scraped data  
- URL‑wise filtering of grouped content in the UI  

## Project Structure

- **app.py** – Streamlit UI and control flow  
- **scraper.py** – Page fetching, CF bypass, parsing, indexing  
- **cloudfare_bypasser.py** – Logic to click through Cloudflare checks  
- **llm.py** – Subquery generation & prompt orchestration with OllamaLLM  
- **requirements.txt** – Python dependencies  
- **.gitignore** – Files/folders to ignore  
- **website_data.json** – (auto‑generated) scraped output  

## Requirements

- Python 3.8+  
- Google Chrome / Chromium installed  
- - Chrome Headless Shell binary (`chrome-headless-shell`)  
- - Place the `chrome-headless-shell` binary in the project root with its dependencies  
- [Ollama](https://ollama.com/) runtime for Llama 3.1    
- Install dependencies:  
  ```bash
  pip install -r requirements.txt
  ```


## Usage

1. Activate your virtual environment  
2. Install dependencies (`pip install -r requirements.txt`)  
3. Populate `.env` as above  
4. Launch the app:
   ```bash
   streamlit run app.py
   ```
5. In the browser:
   - **Step 1:** Paste URLs (one per line) and click **Scrape Site**  
   - **Step 2:** Enter your query; enable “Analyze and break down complex queries” to auto‑split multi‑part questions  

## How It Works

1. **Scraping** (`scraper.py`):  
   - Launches a headless Chromium session  
   - Bypasses Cloudflare challenges via `CloudflareBypasser`  
   - Waits for JS content, inlines iframes, extracts cleaned HTML  
2. **Parsing**: strips navigation/footer, groups by headings (h1–h5)  
3. **Indexing**:  
   - Generates embeddings for titles & content  
   - Builds a FAISS L2 index for nearest‑neighbor search  
4. **Querying** (`llm.py`):  
   - Optionally decomposes complex queries into subqueries  
   - Retrieves top‐k relevant sections from FAISS  
   - Builds a prompt and invokes Llama 3.1 via OllamaLLM  
   - Displays combined or subquery responses  

## Exported Data

- Scraped content is saved as `website_data.json` (overwritten each run)  
- You can adjust the output filename in `app.py` or `scraper.py`
