# Brand Intelligence System

An AI-powered Brand Intelligence System designed to analyze brand identity, understand brand DNA, discover products, and generate intelligent insights using Generative AI.

## 🚀 Overview

The Brand Intelligence System is designed to understand a brand's identity by analyzing its website, brand assets, product information, and creative content.

It uses multiple AI agents and specialized prompt engineering techniques to extract meaningful insights and maintain structured brand knowledge.

## ✨ Key Features

- **Brand Memory:** Maintains structured brand information and context.
- **Brand DNA Analysis:** Extracts brand identity, tone, style, and characteristics.
- **Audience DNA Analysis:** Analyzes target audience information.
- **Content Analysis:** Generates insights from brand content.
- **Creative Analysis:** Analyzes visual creatives and creative patterns.
- **Product Discovery:** Discovers relevant products using browser automation.
- **Product Analysis:** Analyzes product information and attributes.
- **Visual Analysis:** Extracts insights from visual content.
- **Context Management:** Maintains and compresses brand context.
- **Multi-Agent Architecture:** Uses specialized AI agents for different tasks.

## 🛠️ Tech Stack

- Python
- Generative AI (Gemini API)
- Groq API
- Prompt Engineering
- AI Agents
- Playwright
- JSON-based Data Management

## 📁 Project Structure

```text
brand-intelligence-system/
│
├── agents/
├── data/
│   ├── pages/
│   └── screenshots/
│
├── memory/
│   └── brand_memory.json
│
├── outputs/
│
├── prompts/
│
├── services/
│   ├── gemini_service.py
│   ├── groq_service.py
│   ├── playwright_service.py
│   └── product_discovery_service.py
│
├── utils/
│
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd brand-intelligence-system
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows:**
```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and add your API keys:

```env
GEMINI_API_KEY=your_gemini_api_key
GROQ_API_KEY=your_groq_api_key
```

Never upload your actual `.env` file or API keys to GitHub.

### 5. Run the Project

```bash
python main.py
```

## 🔐 Environment Variables

The project uses environment variables to manage API credentials securely.

- `GEMINI_API_KEY`
- `GROQ_API_KEY`

Refer to `.env.example` for the required configuration.

## 🎯 Project Goal

The goal of this project is to build an intelligent brand analysis system that understands brand identity, stores relevant brand knowledge, and generates structured insights through specialized AI agents.

## 👩‍💻 Developer

Purvi Jain

AI Engineer | Generative AI | Python | AI Agents | RAG

---

*Built with Python and Generative AI.*
