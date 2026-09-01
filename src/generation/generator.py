import sys
import os
from pathlib import Path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from pydantic import BaseModel, Field, AliasChoices
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI  # pyright: ignore[reportMissingImports]
from langchain_core.prompts import ChatPromptTemplate  # pyright: ignore[reportMissingImports]
from langchain_core.documents import Document  # pyright: ignore[reportMissingImports]
from utils.helpers import load_config

load_dotenv(override=True)
config = load_config()

class QuizQuestion(BaseModel):
    question: str = Field(description="The multiple choice question text.")
    options: list[str] = Field(description="Exactly 4 options for the student.")
    
    # This alias intercepts the typo 'corrent_answer' from the LLM and maps it to correct_answer safely
    correct_answer: str = Field(
        validation_alias=AliasChoices('correct_answer', 'corrent_answer'),
        description="The exact text of the correct option choice."
    )
    explanation: str = Field(description="A brief explanation of why this answer is correct.")

class TextbookQuiz(BaseModel):
    topic: str = Field(description="The main topic of the quiz.")
    questions: list[QuizQuestion] = Field(description="A list of multiple choice questions.")

def generate_study_material(chunks: list[Document], action_type: str) -> str:
    """
    Synthesizes retrieved textbook chunks into a summary or a quiz specification.
    action_type options: 'summary' or 'quiz'
    """

    try:
        context ="\n\n".join([f"[Source Page {doc.metadata.get('page')}]: {doc.page_content}" for doc in chunks])

        llm = ChatOpenAI(
            model=config["models"]["llm"],
            temperature=config["models"]["temperature"]
        )

        if action_type.lower() == "summary":
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", "You are an expert tutor. Create a comprehensive, highly structured chapter summary using the provided textbook context. Use clear markdown headers, bold terms, and bullet points. Do not assume or extrapolate facts outside the context."),
                ("human", "Textbook Context:\n{context}\n\nGenerate a structured summary highlighting essential concepts, code patterns, and core rules.")
            ])

            chain = prompt_template | llm
            response = chain.invoke({"context": context})
            return response.content

        elif action_type.lower() == "quiz":
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", "You are an academic test designer. Analyze the context and write a one-sentence summary containing the key technical subtopics and terms covered in these pages."),
                ("human", "Textbook Context:\n{context}\n\nProvide the subtopic string:")
            ])
            
            structured_llm = llm.with_structured_output(TextbookQuiz)
            chain = prompt_template | structured_llm
            response = chain.invoke({"context": context})
            return response
            
        else:
            raise ValueError("Invalid action_type. Choose 'summary' or 'quiz'.")


    except Exception as e:
        print(f"Error in generation pipeline: {e}")
        return ""


if __name__ == "__main__":
    from retrieval.retrieval import query_vector_db
    student_query = "Explain how functions work, parameters, arguments, and returning values."
    
    # Track selection: Change this to "summary" or "quiz" to test both endpoints
    selected_action = "quiz" 

    matched_docs = query_vector_db(query=student_query, k=3)

    output = generate_study_material(chunks=matched_docs, action_type=selected_action)
    print(output)