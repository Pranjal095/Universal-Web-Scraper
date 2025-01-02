import streamlit as st
from scraper import perform_scraping,parse_content,save_data,format_data,split_content
from llm import prompt_llm

st.title("Universal Web Scraper Tool")
url = st.text_input("Enter the website's URL")

if st.button("Scrape Site"):
    st.write("Scraping...")
    html = perform_scraping(url)
    grouped_data = parse_content(html)
    save_data(grouped_data, output_file="website_data.json")
    content = format_data(grouped_data)
    st.session_state.dom_content = content
    st.write("Content scraped and formatted")
    
    with st.expander("View Content"):
        st.text_area("Formatted Content",content,height=300)

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe your prompt")

    if st.button("Enter"):
        if parse_description:
            st.write("Parsing the content...")
            content_batches = split_content(st.session_state.dom_content)
            result = prompt_llm(content_batches,parse_description)
            st.write(result)
            st.write("Response generated")   