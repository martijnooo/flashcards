import streamlit as st
from utils.pinecone_utils import initialize_pinecone

def load_css(file_path):
    """Load and apply CSS styles from a file"""
    try:
        with open(file_path, 'r') as f:
            css = f.read()
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file not found: {file_path}")
    except Exception as e:
        st.error(f"Error loading CSS: {e}")

def main():
    st.set_page_config(
        page_title="Flashcard Genius - Home",
        page_icon="🧠",
        layout="wide"
    )

    # Load and apply CSS
    load_css('styles.css')

    try:
        _, _, retriever, vectorstore = initialize_pinecone()
        db_connected = True
    except:
        db_connected = False
    
    # Header Section with Impact
    st.markdown('<h1 class="main-header">🧠 Flashcard Genius</h1>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">AI-Powered Learning • Smart Flashcards • Instant Knowledge</p>', unsafe_allow_html=True)
    
    # Hero Section - Added content between header and problem/solution
    st.markdown("""
    <div style='text-align: center; padding: 0.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; color: white;'>
        <h3 style='color: white; margin-bottom: 0rem;'>Transform How You Learn</h3>
        <p style='font-size: 1rem; opacity: 0.9;'>
        Upload any document and instantly get AI-generated flashcards. No more manual work, no more forgetting what you learn.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Visual Problem/Solution Comparison - Horizontal Layout
    st.markdown("## 🔄 Learning Transformed")
    
    # Problem Cards (Traditional Learning)
    st.markdown("#### 📝 Traditional Learning")
    prob_col1, prob_col2, prob_col3, prob_col4 = st.columns(4)
    
    with prob_col1:
        st.markdown("""
        <div class="stats-card" style="border-top: 4px solid #ff6b6b;">
            <h3>⏰</h3>
            <p>Hours Wasted</p>
            <small>Manual card creation</small>
        </div>
        """, unsafe_allow_html=True)
    
    with prob_col2:
        st.markdown("""
        <div class="stats-card" style="border-top: 4px solid #ff6b6b;">
            <h3>🔄</h3>
            <p>Duplicate Cards</p>
            <small>No organization</small>
        </div>
        """, unsafe_allow_html=True)
    
    with prob_col3:
        st.markdown("""
        <div class="stats-card" style="border-top: 4px solid #ff6b6b;">
            <h3>📚</h3>
            <p>Disorganized</p>
            <small>Scattered knowledge</small>
        </div>
        """, unsafe_allow_html=True)
    
    with prob_col4:
        st.markdown("""
        <div class="stats-card" style="border-top: 4px solid #ff6b6b;">
            <h3>🔍</h3>
            <p>Hard to Search</p>
            <small>No smart search</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Arrow transition
    st.markdown("<div style='text-align: center; font-size: 2rem; color: #667eea; margin: 0rem 0;'>↓</div>", unsafe_allow_html=True)
    
    # Solution Cards (Flashcard Genius)
    st.markdown("#### 🚀 Flashcard Genius")
    sol_col1, sol_col2, sol_col3, sol_col4 = st.columns(4)
    
    with sol_col1:
        st.markdown("""
        <div class="stats-card" style="border-top: 4px solid #667eea;">
            <h3>⚡</h3>
            <p>Instant Generation</p>
            <small>AI creates cards in seconds</small>
        </div>
        """, unsafe_allow_html=True)
    
    with sol_col2:
        st.markdown("""
        <div class="stats-card" style="border-top: 4px solid #667eea;">
            <h3>🔍</h3>
            <p>Smart Detection</p>
            <small>Prevents duplicates automatically</small>
        </div>
        """, unsafe_allow_html=True)
    
    with sol_col3:
        st.markdown("""
        <div class="stats-card" style="border-top: 4px solid #667eea;">
            <h3>📊</h3>
            <p>Organized Knowledge</p>
            <small>AI categorizes everything</small>
        </div>
        """, unsafe_allow_html=True)
    
    with sol_col4:
        st.markdown("""
        <div class="stats-card" style="border-top: 4px solid #667eea;">
            <h3>🎯</h3>
            <p>Semantic Search</p>
            <small>Find anything instantly</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # How It Works - Simple 3-Step Process
    st.markdown("## 🎥 How It Works")
    
    step_col1, step_col2, step_col3 = st.columns(3)
    
    with step_col1:
        st.markdown("""
        <div class="demo-card">
            <div style="text-align: center; font-size: 3rem; margin-bottom: 1rem;">📤</div>
            <h3 style="text-align: center;">1. Upload</h3>
            <p style="text-align: center;">Upload your Word document with study material</p>
        </div>
        """, unsafe_allow_html=True)
    
    with step_col2:
        st.markdown("""
        <div class="demo-card">
            <div style="text-align: center; font-size: 3rem; margin-bottom: 1rem;">🤖</div>
            <h3 style="text-align: center;">2. Generate</h3>
            <p style="text-align: center;">AI instantly creates smart flashcards</p>
        </div>
        """, unsafe_allow_html=True)
    
    with step_col3:
        st.markdown("""
        <div class="demo-card">
            <div style="text-align: center; font-size: 3rem; margin-bottom: 1rem;">🎯</div>
            <h3 style="text-align: center;">3. Learn</h3>
            <p style="text-align: center;">Review, search, and master your knowledge</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Call to Action Section
    st.markdown("## 🚀 Ready to Transform Your Learning?")
    
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h3 style='color: #6c757d; margin-bottom: 2rem;'>
        Stop forgetting what you learn. Start building knowledge that lasts.
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    action_col1, action_col2, action_col3 = st.columns([1, 2, 1])
    
    with action_col2:
        col_left, col_right = st.columns(2)
        with col_left:
            if st.button("🎯 **Try It Now**", use_container_width=True, type="primary"):
                st.switch_page("pages/1_📤_Create_Flashcards.py")
        with col_right:
            if st.button("🔍 **Explore Features**", use_container_width=True):
                st.switch_page("pages/2_🔍_Search_Flashcards.py")

    # Technical Flowchart
    st.markdown("---")
    st.markdown("## 🔧 Behind the Scenes")

    # Create the flowchart
    col1, arrow1, col2, arrow2, col3, arrow3, col4 = st.columns([1, 0.2, 1, 0.2, 1, 0.2, 1])

    with col1:
        st.markdown(
            """
            <div style='text-align: center; background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h3 style='color: #667eea; margin: 0;'>1</h3>
                <h4 style='margin: 0.5rem 0;'>Upload</h4>
                <p style='font-size: 0.9rem; color: #6c757d; margin: 0;'>User provides document</p>
            </div>
            """, 
            unsafe_allow_html=True
        )

    with arrow1:
        st.markdown("<div style='text-align: center; font-size: 1.5rem; color: #667eea;'>→</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(
            """
            <div style='text-align: center; background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h3 style='color: #667eea; margin: 0;'>2</h3>
                <h4 style='margin: 0.5rem 0;'>Generate</h4>
                <p style='font-size: 0.9rem; color: #6c757d; margin: 0;'>AI processes document chunks</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.markdown(
            "<div style='margin-top: 0.5rem; padding: 0.3rem; background: #667eea; color: white; border-radius: 5px; font-size: 0.7rem; text-align: center;'><strong>Tech:</strong> LLM • Parallel Processing</div>", 
            unsafe_allow_html=True
        )

    with arrow2:
        st.markdown("<div style='text-align: center; font-size: 1.5rem; color: #667eea;'>→</div>", unsafe_allow_html=True)

    with col3:
        st.markdown(
            """
            <div style='text-align: center; background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h3 style='color: #667eea; margin: 0;'>3</h3>
                <h4 style='margin: 0.5rem 0;'>Compare</h4>
                <p style='font-size: 0.9rem; color: #6c757d; margin: 0;'>Check against existing cards</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.markdown(
            "<div style='margin-top: 0.5rem; padding: 0.3rem; background: #667eea; color: white; border-radius: 5px; font-size: 0.7rem; text-align: center;'><strong>Tech:</strong> Vector Database • Similarity Search</div>", 
            unsafe_allow_html=True
        )

    with arrow3:
        st.markdown("<div style='text-align: center; font-size: 1.5rem; color: #667eea;'>→</div>", unsafe_allow_html=True)

    with col4:
        st.markdown(
            """
            <div style='text-align: center; background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                <h3 style='color: #667eea; margin: 0;'>4</h3>
                <h4 style='margin: 0.5rem 0;'>Search</h4>
                <p style='font-size: 0.9rem; color: #6c757d; margin: 0;'>Find relevant cards instantly</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.markdown(
            "<div style='margin-top: 0.5rem; padding: 0.3rem; background: #667eea; color: white; border-radius: 5px; font-size: 0.7rem; text-align: center;'><strong>Tech:</strong> Vector Similarity • Semantic Search</div>", 
            unsafe_allow_html=True
        )

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #6c757d; padding: 2rem;'>
        <strong>Flashcard Genius</strong> - Built with ❤️ using Streamlit & Advanced AI | Transform Your Learning Journey
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()