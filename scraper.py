import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time
import json
import re

def perform_scraping(url):
    chrome_driver_path = "./chromedriver"
    chrome_binary_path = "./chrome-headless-shell"
    options = webdriver.ChromeOptions()
    options.binary_location = chrome_binary_path
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

    try:
        driver.get(url)
        print("Page loaded")
        time.sleep(5)
        return driver.page_source
    finally:
        driver.quit()

def clean_text(text):
    return re.sub(r'\s+',' ',text).strip()

def parse_content(html):
    for tag in ["script","style","footer","nav","header"]:
        html = re.sub(r'<{}[^>]*>.*?</{}>'.format(tag, tag),'',html, flags=re.DOTALL)

    inline_tags = ["span","a","em","strong","i","b","u"]
    for tag in inline_tags:
        html = re.sub(r'<{0}[^>]*>(.*?)</{0}>'.format(tag),r'\1',html, flags=re.DOTALL)

    html = clean_text(html)

    soup = BeautifulSoup(html,"html.parser")

    grouped_data = []
    current_group = None

    for element in soup.body.descendants:
        if element.name and element.name in ["h1","h2","h3","h4"]:
            if current_group and current_group["content"]:
                grouped_data.append(current_group)
            current_group = {
                "title": clean_text(element.get_text()),
                "content": []
            }
        elif current_group and element.string and clean_text(element.string):
            cleaned_text = clean_text(element.string)
            if cleaned_text not in current_group["content"] and cleaned_text not in current_group["title"]:
                current_group["content"].append(cleaned_text)

    if current_group and current_group["content"]:
        grouped_data.append(current_group)

    return grouped_data

def save_data(grouped_data,output_file="output.json"):
    with open(output_file,"w",encoding="utf-8") as f:
        json.dump(grouped_data,f,ensure_ascii=False,indent=4)

def format_data(grouped_data):
    formatted_output = []
    for group in grouped_data:
        title = group['title']
        formatted_output.append(f"{title}\n{'-'*len(title)}\n")
        formatted_output.append("\n".join(group['content']))
        formatted_output.append("\n\n")
    return "\n".join(formatted_output).strip()

def split_content(cleaned_content, max_length=6000):
    return [cleaned_content[i:i+max_length] for i in range(0,len(cleaned_content),max_length)]