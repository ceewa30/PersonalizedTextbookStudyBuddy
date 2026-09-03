# 📄 AI Resume Question Generator

An intelligent, production-ready developer tool that extracts text from a PDF resume and automatically leverages a Large Language Model (LLM) pipeline via **LangChain** to generate tailored, highly specific interview questions and ideal structural answers. 

Built using a modern **Gradio** web user interface for simple drag-and-drop operations.

---

## ✨ Features

- **📂 PDF Text Extraction:** In-memory scanning and parsing of uploaded developer resumes using `PyPDF2`.
- **⛓️ LangChain Orchestration:** Leverages modern LangChain Expression Language (LCEL) pipelines to interact with OpenAI's models asynchronously.
- **🛡️ Guaranteed Schema Outputs:** Utilizes `Pydantic` mapping inside the LLM engine to force deterministic, type-safe JSON returns without formatting drops.
- **🎨 Beautiful Gradio UI:** A streamlined, side-by-side interface for drag-and-drop file inputs and clean Markdown rendering outputs.
- **💡 STAR Answer Formatting:** Every generated answer follows the **Situation, Task, Action, Result** standard used by top-tier tech companies.

---

## 🛠️ Tech Stack

- **Core Engine:** Python 3.10+
- **LLM Pipeline:** LangChain Core, LangChain OpenAI SDK
- **Data Validation:** Pydantic v2
- **PDF Extraction:** PyPDF2
- **Frontend UI:** Gradio

---

## 🚀 Getting Started

### 1. Prerequisites

Make sure you have an OpenAI API Key with access to the `gpt-4o-mini` or `gpt-4o` models.

### 2. Installation

Clone this repository and install the project dependencies:

```bash
# Clone the repository
git clone https://github.com
cd resume-qa-generator

# Install dependencies
pip install gradio pypdf2 langchain-openai pydantic
```

### 3. Set Up Environment Variables

Provide your OpenAI API key to the terminal execution environment:

```bash
# Linux/macOS
export OPENAI_API_KEY="your-actual-api-key-here"

# Windows (Command Prompt)
set OPENAI_API_KEY="your-actual-api-key-here"

# Windows (PowerShell)
$env:OPENAI_API_KEY="your-actual-api-key-here"
```

### 4. Running the Application

Launch the local web server:

```bash
python app.py
```

Open your browser and navigate to the local link generated in the terminal output:
```text
http://127.0.0.1:7860
```

---

## 📂 Project Structure

```text
├── app.py              # Main application entry point containing UI & LangChain pipeline
├── README.md           # Project documentation and setup guide
└── requirements.txt    # Optional dependency tracking file
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a pull request with enhancements like vector storage integrations (RAG) or multiple file uploads.
