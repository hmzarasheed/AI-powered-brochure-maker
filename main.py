import os
import requests
import json
from typing import List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import streamlit as st
from openai import OpenAI

# Load environment variables
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

if not (api_key and api_key.startswith('sk-proj-') and len(api_key) > 10):
    st.error("OPENAI_API_KEY not found or invalid. Please set it in your .env file.")
    st.stop()

MODEL = 'gpt-4o-mini'
openai = OpenAI()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:
    """
    A utility class to represent a Website that we have scraped, now with links
    """
    def __init__(self, url):
        self.url = url
        try:
            response = requests.get(url, headers=headers, timeout=10) # Added timeout
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            self.body = response.content
            soup = BeautifulSoup(self.body, 'html.parser')
            self.title = soup.title.string if soup.title else "No title found"
            if soup.body:
                for irrelevant in soup.body(["script", "style", "img", "input", "head", "footer", "nav"]): # Added more tags to remove
                    irrelevant.decompose()
                self.text = soup.body.get_text(separator="\n", strip=True)
            else:
                self.text = ""
            links = [link.get('href') for link in soup.find_all('a')]
            self.links = [link for link in links if link]
        except requests.exceptions.RequestException as e:
            st.error(f"Error accessing {url}: {e}")
            self.body = ""
            self.title = "Error"
            self.text = ""
            self.links = []

    def get_contents(self):
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\n\n"

oneshot_system_prompt = """You are provided with a list of links found on a webpage. \
You are able to decide which of the links would be most relevant to include in a brochure about the company or freelancer offering their services, \
such as links to an About page, or a Company page, or Careers/Jobs pages.\n
You should respond in JSON as in this example:
{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page": "url": "https://another.full.url/careers"}
    ]
}
Make sure not to miss any relevant pages."""

fewshot_system_prompt = """You are provided with a list of links found on a webpage. \
You are able to decide which of the links would be most relevant to include in a brochure about the company or freelancer offering their services, \
such as links to an About page, or a Company page, or Careers/Jobs pages.\n You should respond in JSON as in the following examples:
    Example 1
    ['https://great-comps.com/about-me', 'https://www.linkedin.com/in/great-comp/', 'mailto:hello@mygroovydomain.com', 'https://great-comps.com/news', '/case-studies', 'https://patents.google.com/patent/US20210049536A1/', 'https://great-comps.com/workshop-ai']

    Links:
    {
        "links": [
            {"type": "about page", "url": "https://great-comps.de/about-me"},
            {"type": "news page": "url": "https://great-comps.de/news"},
            {"type": "case studies page": "url": "https://great-comps.de/case-studies"},
            {"type": "workshop page": "url": "https://great-comps.de/workshop-ai"}
        ]
    }

    Example 2
    ['mailto:info@robbie-doodle-domain.com','https://wahlen-robbie.at/ueber-mich', 'https://www.linkedin.com/in/robbie-doodle/', 'https://news.ycombinator.com', 'https://wahlen-robbie.at/neuigkeiten', 'https://twitter.com/robbie-d', '/whitepapers', 'https://patents.google.com/patent/US20210049536A1/', 'https://wahlen-robbie.at/services']

    Links:
    {
        "links": [
            {"type": "über mich", "url": "https://wahlen-robbie.at/ueber-mich"},
            {"type": "aktuelles": "url": "https://wahlen-robbie.at/neuigkeiten"},
            {"type": "whitepaper": "url": "https://wahlen-robbie.at/whitepapers"},
            {"type": "services": "url": "https://wahlen-robbie.at/services"}
        ]
    }
Make sure not to miss any relevant pages."""

def get_links_user_prompt(website):
    user_prompt = f"Here is the list of links on the website of {website.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the company or person offering their services, respond with the full https URL in JSON format. \
Do not include Terms of Service, Privacy, email links or social media links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(website.links)
    return user_prompt

def get_links(url, system_prompt=oneshot_system_prompt):
    website = Website(url)
    if not website.links: # Handle cases where website scraping failed or no links were found
        return {"links": []}

    try:
        response = openai.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": get_links_user_prompt(website)}
            ],
            response_format={"type": "json_object"}
        )
        result = response.choices[0].message.content
        return json.loads(result)
    except Exception as e:
        st.error(f"Error getting links from LLM: {e}")
        return {"links": []}

def get_all_details(url, prompt_type=fewshot_system_prompt):
    result = "Landing page:\n"
    landing_page_website = Website(url)
    result += landing_page_website.get_contents()

    links = get_links(url, prompt_type)
    
    # Handle relative links
    base_url = url.split('/')[0] + '//' + url.split('/')[2]
    
    for link_info in links["links"]:
        link_url = link_info["url"]
        if link_url.startswith('/'):
            full_link_url = base_url + link_url
        elif not link_url.startswith('http'):
            full_link_url = f"{base_url}/{link_url}" # Basic assumption for other relative paths
        else:
            full_link_url = link_url
        
        result += f"\n\n{link_info['type']}\n"
        linked_website = Website(full_link_url)
        result += linked_website.get_contents()
    return result

system_prompt_brochure = """You are an assistant that analyzes the contents of several relevant pages from a company website \
and creates a short brochure about the company for prospective customers, investors and recruits. \
The brochure should be a bit unusual in terms of tone and style, it should astound the reader and pique their interest. Respond in markdown.\
Include details of company culture, customers and careers/jobs if you have the information."""

def get_brochure_user_prompt(company_name, url):
    user_prompt = f"You are looking at a company called: {company_name}\n"
    user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
    
    all_details = get_all_details(url)
    user_prompt += all_details
    user_prompt = user_prompt[:10_000] # Increased truncation for more content
    return user_prompt

def create_brochure(company_name, url):
    with st.spinner("Scraping website and generating brochure..."):
        try:
            response = openai.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system_prompt_brochure},
                    {"role": "user", "content": get_brochure_user_prompt(company_name, url)}
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"Error generating brochure with LLM: {e}")
            return None

# Streamlit UI
st.set_page_config(page_title="Company Brochure Generator", layout="wide")

st.title("Company Brochure Generator")

st.markdown("""
This application generates an "unusual" and intriguing brochure for a company based on its website content.
Enter the company name and URL below.
""")

company_name = st.text_input("Company Name", "Edward Donner")
company_url = st.text_input("Company Website URL", "https://edwarddonner.com")

if st.button("Generate Brochure"):
    if company_name and company_url:
        brochure = create_brochure(company_name, company_url)
        if brochure:
            st.markdown("---")
            st.subheader(f"Brochure for {company_name}")
            st.markdown(brochure)
    else:
        st.warning("Please enter both company name and URL.")

st.markdown("---")
st.markdown("### How it works:")
st.markdown("""
1. **Scraping**: The application scrapes the provided website's landing page and extracts all internal links.
2. **Link Selection (LLM)**: An LLM (OpenAI's GPT-4o-mini) analyzes these links and identifies relevant pages for a brochure (e.g., About Us, Careers, Services).
3. **Content Extraction**: The content from these selected relevant pages is then extracted.
4. **Brochure Generation (LLM)**: Finally, another LLM generates a brochure based on the extracted content, with a unique and intriguing tone.
""")