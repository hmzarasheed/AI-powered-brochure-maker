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

### 1. Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Set up your OpenAI API key:
Create a `.env` file in the root directory with the following content:
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx
```


1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**:
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

## 💻 Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📋 Example

Input:
- Company Name: `Edward Donner`
- Company URL: `https://edwarddonner.com`

Output:
- A markdown brochure covering the company’s mission, services, culture, and opportunities — written in a unique, captivating style.

---

## 🧠 How It Works

1. **Scraping**: Grabs the homepage and internal links.
2. **LLM Link Selection**: GPT-4o-mini selects relevant brochure-worthy pages.
3. **Content Collection**: Extracts text from those pages.
4. **Brochure Generation**: GPT composes a concise, markdown-based brochure.

---

## ⚠️ Notes

- Only works with publicly accessible websites.
- Social, email, and legal links are ignored.
- Content is truncated if too long (limited to 10,000 tokens).
