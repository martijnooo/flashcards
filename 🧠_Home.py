import streamlit as st
from utils.pinecone_utils import initialize_pinecone

def main():
    st.set_page_config(
        page_title="Flashcard Genius - Home",
        page_icon="🧠",
        layout="wide"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 2rem;
        color: white;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        height: 100%;
    }
    .step-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #1f77b4;
    }
    .quote-card {
        background: linear-gradient(135deg, #ffd89b 0%, #19547b 100%);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        color: white;
        text-align: center;
        font-style: italic;
    }
    /* Ensure columns have equal height */
    .stColumn {
        display: flex;
        flex-direction: column;
    }
    </style>
    """, unsafe_allow_html=True)

    _, _, retriever, vectorstore = initialize_pinecone()
    
    # Header Section
    st.markdown('<h1 class="main-header">🧠 Welcome to Flashcard Genius</h1>', unsafe_allow_html=True)
    st.markdown("## Transform Your Learning Experience")
    
    st.markdown("""
    **Flashcard Genius** is your intelligent study companion that helps you create, organize, and master knowledge 
    through AI-powered flashcards. Say goodbye to manual note-taking and hello to efficient, smart learning!
    """)
    
    st.markdown("---")
    
    # How It Works Section
    st.markdown("## 🚀 How It Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>1. 📤 Create</h3>
            <p>Upload your study materials and let our AI instantly generate comprehensive flashcards.</p>
            <p><strong>No more tedious manual entry!</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>2. 🔍 Organize</h3>
            <p>Our smart system automatically checks for duplicates and helps you maintain a clean knowledge base.</p>
            <p><strong>Stay organized effortlessly!</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>3. 💾 Master</h3>
            <p>Review and save your flashcards to build a personalized learning database.</p>
            <p><strong>Learn smarter, not harder!</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Key Features Section
    st.markdown("## ✨ Key Features")
    
    features_col1, features_col2 = st.columns(2)
    
    with features_col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI-Powered Generation</h3>
            <ul>
            <li><strong>Instant card creation</strong> from your documents</li>
            <li><strong>Smart content understanding</strong> that captures key concepts</li>
            <li><strong>Structured formatting</strong> with questions and answers</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>💾 Organized Knowledge Base</h3>
            <ul>
            <li><strong>Easy saving</strong> to your personal database</li>
            <li><strong>Category organization</strong> for better recall</li>
            <li><strong>Quick retrieval</strong> when you need to review</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with features_col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🔍 Intelligent Duplicate Detection</h3>
            <ul>
            <li><strong>Automatic similarity checking</strong> across your entire collection</li>
            <li><strong>Smart warnings</strong> to prevent redundant cards</li>
            <li><strong>Similarity scoring</strong> to help you make informed decisions</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Perfect For</h3>
            <ul>
            <li><strong>Students</strong> preparing for exams</li>
            <li><strong>Professionals</strong> learning new skills</li>
            <li><strong>Researchers</strong> organizing knowledge</li>
            <li><strong>Lifelong learners</strong> building expertise</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Call to Action Section
    st.markdown("## 📈 Start Your Learning Journey")
    
    st.markdown("""
    **Ready to transform how you learn?** Choose your path below:
    """)
    
    action_col1, action_col2 = st.columns([1, 1])
    
    with action_col1:
        if st.button("🚀 **Get Started**", use_container_width=True, help="Create new flashcards from your documents"):
            st.switch_page("pages/1_📤_Create_Flashcards.py")
    
    with action_col2:
        if st.button("🔍 **Search Cards**", use_container_width=True, help="Search through your flashcard collection"):
            st.switch_page("pages/2_🔍_Search_Flashcards.py")
    
    # Inspirational Quote
    st.markdown("---")
    st.markdown("""
    <div class="quote-card">
        <h3>"Education is the most powerful weapon which you can use to change the world."</h3>
        <h4>— Nelson Mandela</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6c757d;'>
    <strong>Flashcard Genius</strong> - Built with ❤️ using Streamlit | AI-Powered Learning System
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()