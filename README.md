# 📚 Local AI Study Assistant: Context-Anchored RAG System

An advanced, local web-based AI assistant built to process educational textbooks and notes. By utilizing a **Retrieval-Augmented Generation (RAG)** pipeline, this system eliminates general LLM hallucinations via strict contextual anchoring, providing students with reliable study aids, interactive quizzes, and structured chapter summaries with exact source attribution.

---

## 🗺️ System Architecture

```text
[ PHASE 1: DATA INGESTION PIPELINE ]
  📁 Upload Textbook (PDFs) 
         │
         ▼
  ✂️ Text Splitting (Fixed-size overlap chunking + Page Tracking)
         │
         ▼
  🧠 Embedding Model (e.g., text-embedding-3-small / local BGE)
         │
         ▼
  🗄️ Local Vector Database (ChromaDB)

[ PHASE 2: RETRIEVAL & GENERATION PIPELINE ]
  🧑‍🎓 Student Input  ──► [ Action Type Selection: Quiz or Summary ]
         │
         ▼
  🔍 Query Embedding  ──► [ Semantic Search in Vector DB ]
                                │
                                ▼
                         📑 Top-K Relevant Text Chunks
                                │
                                ▼
  🤖 LLM Generator (OpenAI gpt-4o-mini OR Local Llama 3 via Ollama)
         │
         ▼
  📝 Final Output: Interactive Quiz (with grading) OR Structured Chapter Summary
```

---

## 🎯 Project Objectives

* **Zero Hallucination:** Enforce a strict boundary on the LLM to generate responses derived *only* from the uploaded context.
* **Granular Tracking:** Deliver precise page-level and text-chunk attribution for every generated query, study guide, or quiz question.
* **Automated Study Aids:** Dynamically transform long-form textbook chapters into actionable learning materials (MCQs, flashcards, summaries).
* **Local-First Design:** Provide flexibility for offline operation using open-source, local vector databases and local LLMs to prioritize data privacy.

---

## 🗂️ Core Features

* **Document Ingestion Portal:** A seamless drag-and-drop dashboard in the browser built to process large, multi-page educational PDFs.
* **Smart Chunker:** Layout-aware parsing that cleanly processes page boundaries and respects tabular structures without breaking text context.
* **Interactive Evaluation Dashboard:** A dynamic workspace where users select output goals (e.g., *"Generate a 5-question quiz for Chapter 3"*), take the quiz interactively, and receive instant grading.
* **Source Attribution Matrix:** Every summary bullet point or quiz question includes a collapsible section mapping back to its exact origin block and page number in the source material.

---

## 🛠️ Technical Stack

* **Frontend Dashboard:** [Gradio](https://gradio.app/) (Python-based interactive UI)
* **RAG Orchestration:** [LlamaIndex](https://llamaindex.ai) / [LangChain](https://langchain.com)
* **Vector Storage:** [ChromaDB](https://trychroma.com) (Local persistent database)
* **LLM Engines:** 
  * **Cloud:** OpenAI `gpt-4o-mini` (High speed & reasoning)
  * **Local:** [Ollama](https://ollama.com) running `llama3:8b` (Data privacy & zero API cost)

---

## 🚀 Getting Started

### Prerequisites
* Python 3.10 or higher
* (Optional) [Ollama installed](https://ollama.com) if running fully locally.

### 1. Clone the Repository
```bash
git clone https://github.com
cd local-ai-study-assistant
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file in the root directory:
```env
# For OpenAI Cloud Execution
OPENAI_API_KEY=your_openai_api_key_here

# For Local Execution (Ollama default endpoint)
OLLAMA_BASE_URL=http://localhost:11434
```

### 4. Run the Application
```bash
uv run gradio app.py
```

---

## 🔒 Contextual Anchoring Guardrails

The engine uses strict system prompt routing to ensure safety against hallucinations:
1. **Context Constraining:** "Answer the student's request using ONLY the provided textbook context. If the answer cannot be derived, output: *'Information not found in the uploaded text.'*"
2. **Metadata Binding:** The vector database payload injects metadata payloads (`{source: file.pdf, page: X}`) into the retrieved nodes before passing them to the LLM context window.
