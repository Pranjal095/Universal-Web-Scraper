import streamlit as st
from scraper import scrape_page, parse_content, save_data, build_index, retrieve_relevant_sections
from llm import prompt_llm

st.title("Universal Web Scraper Tool")
st.markdown("""
This tool allows you to scrape website content, index it, and query relevant information using an LLM.
- **Step 1:** Enter one or more URLs to scrape (one per line).
- **Step 2:** Submit queries to extract relevant information interactively.
""")

st.subheader("Step 1: Scrape Website")
urls = st.text_area("Enter website URL(s) (one per line)")

if st.button("Scrape Site"):
    if urls.strip():
        urls_list = [url.strip() for url in urls.split("\n") if url.strip()]
        
        if not urls_list:
            st.error("Please enter at least one valid URL.")
        else:
            all_grouped_data = []
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, url in enumerate(urls_list):
                status_text.text(f"Processing URL {i+1}/{len(urls_list)}: {url}")
                
                try:
                    html = scrape_page(url)
                    current_grouped_data = parse_content(html)
                    
                    for section in current_grouped_data:
                        section["source_url"] = url
                    
                    all_grouped_data.extend(current_grouped_data)
                    
                    progress_bar.progress((i + 1) / len(urls_list))
                    
                except Exception as e:
                    st.error(f"Error processing {url}: {str(e)}")
            
            if all_grouped_data:
                indexed_data = build_index(all_grouped_data)
                save_data(all_grouped_data, output_file="website_data.json")
                st.session_state.indexed_data = indexed_data
                st.session_state.grouped_data = all_grouped_data
                st.session_state.scraped = True
                status_text.text("Processing complete!")
                st.success(f"Content scraped from {len(urls_list)} URLs, indexed, and ready for queries!")
            else:
                st.error("No content could be scraped from the provided URLs.")
    else:
        st.error("Please enter at least one URL.")

if "grouped_data" in st.session_state:
    st.subheader("View Scraped Content")
    with st.expander("Grouped Content"):
        if any("source_url" in item for item in st.session_state.grouped_data):
            urls_in_data = list(set(item.get("source_url", "") for item in st.session_state.grouped_data))
            selected_url = st.selectbox("Filter by URL", ["All URLs"] + urls_in_data)
            
            if selected_url != "All URLs":
                filtered_data = [item for item in st.session_state.grouped_data 
                                if item.get("source_url", "") == selected_url]
                st.json(filtered_data)
            else:
                st.json(st.session_state.grouped_data)
        else:
            st.json(st.session_state.grouped_data)

if "indexed_data" in st.session_state:
    st.subheader("Step 2: Query the Website Content")
    query = st.text_area("Enter your query", key="query_input")

    if st.button("Submit Query", key="submit_query"):
        if query.strip():
            st.write("Retrieving relevant content...")
            relevant_sections = retrieve_relevant_sections(query, st.session_state.indexed_data)
            st.write("Generating response...")
            result = prompt_llm(relevant_sections, query)
            st.write(result)

            if "queries" not in st.session_state:
                st.session_state.queries = []
            st.session_state.queries.append({"query": query, "response": result})
            
            st.success("Response generated!")
        else:
            st.error("Please enter a valid query.")

    if "queries" in st.session_state and st.session_state.queries:
        st.subheader("Query History")
        for i, entry in enumerate(st.session_state.queries):
            with st.expander(f"Query {i+1}: {entry['query']}"):
                st.markdown(f"**Response:**\n\n{entry['response']}")