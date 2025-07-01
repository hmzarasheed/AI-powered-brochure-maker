# 🏢 Company Brochure Generator

A Streamlit application that intelligently scrapes a company's website, analyzes its content using OpenAI's GPT model, and generates an engaging, unusual, markdown-style brochure for potential customers, investors, or recruits.

---

## 🚀 Features

- 🌐 **Web Scraping**: Extracts the main landing page and all internal links from a provided company website.
- 🧠 **LLM-Powered Link Filtering**: Uses OpenAI's GPT-4o-mini to select only relevant links (e.g., About, Services, Careers) for brochure creation.
- 📄 **Content Extraction**: Collects textual content from the selected pages using BeautifulSoup.
- 📝 **AI Brochure Generation**: GPT-4o-mini crafts a compelling brochure with a unique tone using the scraped content.
- 📺 **Streamlit UI**: Simple and interactive web interface to generate brochures in real-time.

---

## 🧱 Tech Stack

- **Python**
- **Streamlit** - for interactive UI
- **BeautifulSoup** - for HTML parsing
- **Requests** - for HTTP calls
- **OpenAI API** - for GPT-4o-mini chat completions
- **dotenv** - for secure API key handling

---

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
