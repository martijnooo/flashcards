from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from utils.env_loader import load_env, get_env_var
import streamlit as st

@st.cache_resource
def create_llm():
    load_env()
    return ChatOpenAI(model="gpt-4o-mini", api_key=get_env_var("OPENAI_API_KEY"), temperature=0)

def generate_flashcards(llm, text_chunk: str):
    prompt = ChatPromptTemplate.from_template("""
            You are a flashcard generator.
            Given the text below, generate diverse Q&A flashcards with different question types, including a category that best suits the topic. Keep the number of flashcards generated reasonable. If there is a lot of content, create more, otherwise less.

            Each flashcard should have this JSON structure:
            [
            {{
                "question": "...",
                "answer": "...",
                "category": "...",
                "type": "..."  // One of: "multiple_choice", "true_false", "fill_blank", "short_answer", "matching"
            }}
            ]

            QUESTION TYPES AND EXAMPLES:

            1. MULTIPLE CHOICE:
            {{
            "question": "What is the primary function of the mitochondria?",
            "answer": "C) Produce energy (ATP)",
            "category": "Biology",
            "type": "multiple_choice"
            }}
            // Format: Include options A, B, C, D in the question or answer

            2. TRUE/FALSE:
            {{
            "question": "The Earth is the largest planet in our solar system.",
            "answer": "False",
            "category": "Astronomy",
            "type": "true_false"
            }}

            3. FILL IN THE BLANK:
            {{
            "question": "The process of liquid turning into gas is called ______.",
            "answer": "evaporation",
            "category": "Chemistry",
            "type": "fill_blank"
            }}

            4. SHORT ANSWER (standard):
            {{
            "question": "What is photosynthesis?",
            "answer": "The process by which plants convert sunlight into chemical energy",
            "category": "Biology",
            "type": "short_answer"
            }}

            5. MATCHING:
            {{
            "question": "Match the programming languages to their primary use: Python, JavaScript, SQL",
            "answer": "Python: Data Science, JavaScript: Web Development, SQL: Database Management",
            "category": "Computer Science",
            "type": "matching"
            }}

            6. DEFINITION:
            {{
            "question": "Define 'cognitive dissonance'",
            "answer": "The mental discomfort experienced when holding conflicting beliefs",
            "category": "Psychology",
            "type": "short_answer"
            }}

            7. PROCESS/SEQUENCE:
            {{
            "question": "What are the stages of mitosis in order?",
            "answer": "Prophase, metaphase, anaphase, telophase",
            "category": "Biology",
            "type": "short_answer"
            }}

            GUIDELINES FOR EACH TYPE:
            - Multiple Choice: Create plausible distractors, mark correct answer clearly
            - True/False: Make statements that are clearly true or false
            - Fill Blank: Place blank where key term should go
            - Matching: Group related items that need to be paired
            - Short Answer: Focus on key concepts and definitions

            Return ONLY valid JSON — no explanations, markdown, or text outside the JSON.

            Text:
            {text}
            """)

    chain = prompt | llm
    output = chain.invoke({"text": text_chunk}).content.strip()
    return output
