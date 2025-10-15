import streamlit as st
from utils.pinecone_utils import initialize_pinecone

# Load CSS from file
def load_css(file_path):
    with open(file_path, 'r') as f:
        return f.read()

# Flashcard rendering
def render_flashcard(col, result):
    col.markdown(
        f'<div class="flashcard-container"> Q: {result.page_content}</div>',
        unsafe_allow_html=True
    )
    with col.expander("Show Answer", icon="🔍"):
        st.markdown(f"**A:** {result.metadata['answer']}")

# Page configuration
st.set_page_config(
    page_title="Search Flashcards",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load and apply CSS
css = load_css('styles.css')
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Initialize Pinecone (runs once)
_, _, retriever, vectorstore = initialize_pinecone()

# Header
st.markdown('<h1 class="main-header">🔍 Flashcard Search</h1>', unsafe_allow_html=True)

query = st.text_input("What would you like to learn about?")

if query:
    with st.spinner("🤖 Retrieving flashcards from database..."):
        try:
            results = retriever.invoke(query)

            if not results:
                st.write("No flashcards on that topic found 🥲")
            else:
                cols = st.columns(2)
                for i, result in enumerate(results):
                    render_flashcard(cols[i % 2], result)

        except Exception as e:
            st.error(f"Error retrieving documents: {e}")
