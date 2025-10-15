import streamlit as st
from utils.text_utils import split_text, safe_parse_json, read_word
from utils.llm_utils import create_llm, generate_flashcards
from utils.pinecone_utils import initialize_pinecone, upsert_flashcards

# Load CSS from file
def load_css(file_path):
    with open(file_path, 'r') as f:
        return f.read()

# Page configuration
st.set_page_config(
    page_title="Flashcard Generator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load and apply CSS
css = load_css('styles.css')
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🧠 Flashcard Generator</h1>', unsafe_allow_html=True)

# Sidebar for instructions
with st.sidebar:
    st.markdown("### 📖 How to Use")
    st.markdown("""
    1. **Upload** a Word document with your study material
    2. **Generate** flashcards automatically from the content
    3. **Review** each flashcard with answers
    4. **Check** for similar existing cards
    5. **Save** unique cards to your database
    """)
    
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Upload well-structured documents for best results
    - Review similar cards before saving to avoid duplicates
    """)

# Initialize session state
if 'flashcards_generated' not in st.session_state:
    st.session_state.flashcards_generated = False
if 'current_flashcards' not in st.session_state:
    st.session_state.current_flashcards = []
if 'added_to_db' not in st.session_state:
    st.session_state.added_to_db = {}
if 'similar_cards' not in st.session_state:
    st.session_state.similar_cards = {}
if 'show_generator' not in st.session_state:
    st.session_state.show_generator = True

# Toggle for generator section
col_toggle1, col_toggle2, col_toggle3 = st.columns([1, 2, 1])
with col_toggle2:
    toggle_label = "📥 Hide Generator" if st.session_state.show_generator else "📤 Show Generator"
    if st.button(toggle_label, use_container_width=True):
        st.session_state.show_generator = not st.session_state.show_generator
        st.rerun()

# Generator section in expander
if st.session_state.show_generator:
    with st.expander("🚀 Flashcard Generator", expanded=True):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown('<h2 class="sub-header">📤 Upload Document</h2>', unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "Choose a Word document", 
                type=['docx', 'doc'],
                help="Upload a .docx or .doc file to generate flashcards from"
            )

            if uploaded_file:
                with st.expander("📄 Document Preview", expanded=False):
                    text = read_word(uploaded_file)
                    st.text_area(
                        "Extracted Text", 
                        text, 
                        height=200,
                        label_visibility="collapsed"
                    )
        
        with col2:
            if uploaded_file:
                st.markdown('<h2 class="sub-header">🎯 Generation</h2>', unsafe_allow_html=True)
                # Generate button centered
                _, generate_col, _ = st.columns([1, 2, 1])
                with generate_col:
                    generate = st.button(
                        "🚀 Generate Flashcards", 
                        type="primary",
                        use_container_width=True,
                        help="Click to generate flashcards from the uploaded document"
                    )
            else:
                st.info("📝 Please upload a Word document to generate flashcards")

        if uploaded_file and generate:
            with st.spinner("🤖 Generating flashcards from your document..."):
                chunks = split_text(text)
                llm = create_llm()
                flashcards = []
                for chunk in chunks:
                    raw_output = generate_flashcards(llm, chunk)
                    flashcards += safe_parse_json(raw_output)
                
                # Store in session state
                st.session_state.current_flashcards = flashcards
                st.session_state.flashcards_generated = True
                # Reset the tracking dictionaries when new flashcards are generated
                st.session_state.added_to_db = {i: False for i in range(len(flashcards))}
                st.session_state.similar_cards = {}
                
                st.toast(f"✅ Successfully generated {len(flashcards)} flashcards!")
                # Auto-collapse the generator after successful generation
                st.session_state.show_generator = False
                st.rerun()

# Display flashcards from session state - FULL WIDTH
if st.session_state.flashcards_generated:
    st.markdown("---")
    st.markdown('<h2 class="sub-header">📚 Generated Flashcards</h2>', unsafe_allow_html=True)
    
    # Stats bar
    total_cards = len(st.session_state.current_flashcards)
    added_cards = sum(st.session_state.added_to_db.values())
    duplicate_cards = sum(1 for i in st.session_state.similar_cards if st.session_state.similar_cards[i] is not None)
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    with stat_col1:
        st.metric("Total Cards", total_cards)
    with stat_col2:
        st.metric("Added to DB", added_cards)
    with stat_col3:
        st.metric("Potential Duplicates", duplicate_cards)
    with stat_col4:
        st.metric("Remaining", total_cards - added_cards)
    
    # Initialize Pinecone components
    index, embedder, _, vectorstore = initialize_pinecone()
    
    # Display flashcards in a grid for better use of full width
    cols_per_row = 2  # You can adjust this to 1 for single column or 2 for two columns
    flashcards = st.session_state.current_flashcards
    
    for i in range(0, len(flashcards), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            if i + j < len(flashcards):
                with cols[j]:
                    flashcard = flashcards[i + j]
                    index_pos = i + j
                    
                    # Check for similar cards if not already checked
                    if index_pos not in st.session_state.similar_cards:
                        similar = vectorstore.similarity_search_with_score(flashcard["question"], k=1)
                        st.session_state.similar_cards[index_pos] = similar[0] if similar and similar[0][1] > 0.87 else None
                    
                    similar_card_data = st.session_state.similar_cards[index_pos]
                    is_duplicate = similar_card_data is not None
                    
                    # Use Streamlit container
                    container = st.container()
                    
                    with container:
                        st.markdown(f'<div class="flashcard-container"> Q: {flashcard['question']}', unsafe_allow_html=True)
                        
                        # Answer section
                        with st.expander("Show Answer", icon="🔍"):
                            # Answer content
                            st.markdown(f"**A:** {flashcard['answer']}")
                            
                            # Metadata
                            meta_col1, meta_col2 = st.columns(2)
                            with meta_col1:
                                if flashcard.get('category'):
                                    st.markdown(f"**Category:** `{flashcard['category']}`")
                            with meta_col2:
                                if flashcard.get('type'):
                                    st.markdown(f"**Type:** `{flashcard['type']}`")
                            
                            # Display similar card details if duplicate detected
                            if is_duplicate:
                                similar_card = similar_card_data[0]
                                similarity_score = similar_card_data[1]
                                st.markdown("---")
                                st.markdown("**🔍 Similarity Check Results:**")
                                st.warning(f"**Similarity Score:** {similarity_score:.3f}")
                                st.info(f"**Existing similar card in database:** {similar_card.page_content}")

                        # Action buttons
                        col_left, _, col_right = st.columns([2, 1, 1])
                        
                        with col_left:
                            is_disabled = st.session_state.added_to_db.get(index_pos, False)
                            
                            if is_disabled:
                                st.success("✅ Added to Database")
                            else:
                                if st.button("💾 Save to Database", key=f"add_{index_pos}", use_container_width=True):
                                    with st.spinner("Saving to database..."):
                                        upsert_flashcards(index, embedder, [flashcard])
                                        st.toast(
                                            f"✅ Flashcard added to database: {flashcard['question']}", 
                                            icon='🧠'
                                        )
                                        st.session_state.added_to_db[index_pos] = True
                                        st.rerun()
                        with col_right:
                            if is_duplicate:
                                st.markdown('<div class="duplicate-label">⚠️ Possible Duplicate</div>', unsafe_allow_html=True)

# Show message when no flashcards generated
elif not st.session_state.show_generator:
    st.info("🎯 Use the 'Show Generator' button above to upload a document and generate flashcards")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #6c757d;'>"
    "Built with ❤️ using Streamlit | Flashcard Learning System"
    "</div>",
    unsafe_allow_html=True
)