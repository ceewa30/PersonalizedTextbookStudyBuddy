🗺️ System Architecture Diagram

[ PHASE 1: DATA INGESTION PIPELINE ]
  📁 Upload Textbook (PDFs) 
         │
         ▼
  ✂️ Text Splitting (Fixed-size overlap chunking)
         │
         ▼
  🧠 Embedding Model (e.g., text-embedding-3-small)
         │
         ▼
  🗄️ Local Vector Database (ChromaDB / FAISS)

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
  🤖 LLM Generator (OpenAI / Llama 3 with customized prompt template)
         │
         ▼
  📝 Final Output: Interactive Quiz (with answers) OR Structured Chapter Summary




  📋 Capstone Project Outline
  
  🎯 Project Objectives
  
  Build a local web-based AI assistant capable of processing standard educational textbooks and notes.

  Eliminate general LLM hallucinations by strict contextual anchoring.
  
  Automate the generation of formatted study aids (multiple-choice quizzes, key concept flashcards, and chapter summaries).
  
  🗂️ Core Feature Requirements
  
  Document Ingestion Portal: A drag-and-drop dashboard for uploading large PDF textbooks.
  
  Smart Chunker: Preprocesses textual layouts, handling page boundaries and tables gracefully.
  
  Contextual Flashcard & Quiz Builder: A dynamic selector where students can request "Generate a 5-question quiz for Chapter 3".
  
  Source Attribution: Each generated summary or quiz must explicitly link to the exact page number or source chunk text it pulled from.
  
  🛠️ Technical Stack Recommendations
  
  Frontend Dashboard: Streamlit or Gradio (Python-based, zero-CSS frameworks).
  
  RAG Orchestration Framework: LangChain or LlamaIndex.
  
  Vector Storage: ChromaDB or local file-based FAISS.
  
  LLM Engine: gpt-4o-mini API for production quality, or Ollama running Llama 3 (8B) locally to prevent data privacy issues.
  
  📈 Phased Implementation Plan
  
  Phase             Focus               Core Deliverables
  
  Phase 1         Data Preprocessing    Set up PDF reader, configure RecursiveCharacterTextSplitter, 
                                        test vector conversion.
  
  Phase 2         DB Storage &          Initialize local ChromaDB instance; construct 
                  Retrieval             query system with similarity_search.
  
  Phase 3         Prompt Engineering    Write strict system prompts (e.g., "You are an AI teacher.
                                        Only use the retrieved context. If unsure, say 'Not found in textbook'").
  
  Phase 4         Interactive UI        Build the Streamlit interface with 
                  Development           distinct tabs for uploading, testing, and viewing metrics.
  
  Phase 5         Evaluation &          Run basic accuracy validation using Ragas 
                  Fine-tuning           frameworks or manual sample testing.

  