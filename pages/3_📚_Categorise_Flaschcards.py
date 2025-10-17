import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from collections import Counter
from utils.pinecone_utils import initialize_pinecone

# Initialize Pinecone
index = initialize_pinecone()

# Load CSS from file
def load_css(file_path):
    with open(file_path, 'r') as f:
        return f.read()
# Load and apply CSS
css = load_css('styles.css')
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🧠 Flashcard Category Analysis</h1>',  unsafe_allow_html=True)

try:
    # Retrieve all flashcards
    with st.spinner("Retrieving flashcards from database..."):
        all_flashcards = index[0].query(
            vector=[0]*1536,  # dummy vector of same dimension
            top_k=500,        # adjust based on your dataset size
            include_metadata=True,
            include_values=True  # Important for clustering
        )
    
    # Extract data from metadata
    categories = []
    cards_data = []
    vectors = []
    
    for match in all_flashcards.matches:
        metadata = match.metadata
        if metadata and 'category' in metadata:
            category = metadata['category']
            categories.append(category)
            cards_data.append({
                'id': match.id,
                'category': category,
                'score': match.score,
                'metadata': metadata
            })
            vectors.append(match.values)
    
    # Convert to numpy array for clustering
    vectors = np.array(vectors)
    
    # Calculate statistics
    total_cards = len(cards_data)
    category_counts = Counter(categories)
    unique_categories = len(category_counts)
    
    # Display overall statistics
    st.header("Overall Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Cards", total_cards)
    
    with col2:
        st.metric("Unique Categories", unique_categories)
    
    with col3:
        avg_cards_per_category = total_cards / unique_categories if unique_categories > 0 else 0
        st.metric("Avg Cards per Category", f"{avg_cards_per_category:.1f}")
    
    # Display category breakdown
    st.header("Category Breakdown")
    
    if category_counts:
        # Create a sorted list of categories by count (descending)
        sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Display as a table
        st.subheader("Categories Table")
        category_data = []
        for category, count in sorted_categories:
            category_data.append({
                "Category": category,
                "Card Count": count,
                "Percentage": f"{(count/total_cards)*100:.1f}%"
            })
        
        st.dataframe(category_data)

        with st.expander(label="Show Cluster Analysis"):
            # Display as bar chart
            st.subheader("Categories Distribution")
            chart_data = {
                "Category": [cat for cat, count in sorted_categories],
                "Count": [count for cat, count in sorted_categories]
            }
            st.bar_chart(chart_data, x="Category", y="Count")
        
            # K-means Clustering Section
            st.header("🎯 K-means Clustering Analysis")
            
            if len(vectors) > 0:
                # Sidebar controls for clustering
                st.sidebar.header("Clustering Settings")
                
                max_k = st.sidebar.slider(
                    "Maximum number of clusters to test", 
                    min_value=3, 
                    max_value=min(15, len(vectors)), 
                    value=8,
                    help="Higher values will test more cluster possibilities"
                )
                
                auto_detect = st.sidebar.checkbox("Auto-detect optimal clusters", value=True)
                
                if not auto_detect:
                    manual_k = st.sidebar.slider(
                        "Manual cluster selection", 
                        min_value=2, 
                        max_value=min(10, len(vectors)), 
                        value=4
                    )
                
                # Elbow Method Analysis
                st.subheader("Elbow Method Analysis")
                
                with st.spinner("Calculating optimal clusters..."):
                    # Calculate inertias for different k values
                    inertias = []
                    k_range = range(1, max_k + 1)
                    
                    for k in k_range:
                        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                        kmeans.fit(vectors)
                        inertias.append(kmeans.inertia_)
                    
                    # Plot elbow method
                    fig1, ax1 = plt.subplots(figsize=(10, 6))
                    ax1.plot(k_range, inertias, 'bo-', linewidth=2, markersize=8)
                    ax1.set_xlabel('Number of Clusters (k)')
                    ax1.set_ylabel('Inertia (Within-cluster sum of squares)')
                    ax1.set_title('Elbow Method for Optimal k')
                    ax1.grid(True, alpha=0.3)
                    st.pyplot(fig1)
                
                # Silhouette Analysis
                st.subheader("Silhouette Analysis")
                
                with st.spinner("Calculating silhouette scores..."):
                    silhouette_scores = []
                    k_range_silhouette = range(2, max_k + 1)
                    
                    for k in k_range_silhouette:
                        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                        cluster_labels = kmeans.fit_predict(vectors)
                        silhouette_avg = silhouette_score(vectors, cluster_labels)
                        silhouette_scores.append(silhouette_avg)
                    
                    # Plot silhouette scores
                    fig2, ax2 = plt.subplots(figsize=(10, 6))
                    ax2.plot(k_range_silhouette, silhouette_scores, 'ro-', linewidth=2, markersize=8)
                    ax2.set_xlabel('Number of Clusters (k)')
                    ax2.set_ylabel('Silhouette Score')
                    ax2.set_title('Silhouette Analysis for Optimal k')
                    ax2.grid(True, alpha=0.3)
                    st.pyplot(fig2)
                
            # Determine optimal k
            if auto_detect:
                # Find optimal k from silhouette scores (higher is better)
                optimal_k = k_range_silhouette[np.argmax(silhouette_scores)]
                st.success(f"🎯 Auto-detected optimal number of clusters: **{optimal_k}**")
            else:
                optimal_k = manual_k
                st.info(f"🔧 Using manually selected clusters: **{optimal_k}**")
            
        # Apply K-means clustering
        st.subheader("Clustering Results")
        
        with st.spinner(f"Applying K-means with {optimal_k} clusters..."):
            kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
            cluster_labels = kmeans.fit_predict(vectors)
            
            # Add cluster labels to cards data
            for i, card in enumerate(cards_data):
                card['cluster'] = int(cluster_labels[i])
        
        # Display cluster distribution
        cluster_counts = Counter(cluster_labels)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Number of Clusters", optimal_k)
            st.metric("Total Cards Clustered", len(cluster_labels))
        
        with col2:
            avg_cluster_size = len(cluster_labels) / optimal_k
            st.metric("Average Cluster Size", f"{avg_cluster_size:.1f}")
            largest_cluster = max(cluster_counts.values())
            st.metric("Largest Cluster", largest_cluster)
        
        # Cluster distribution chart
        st.subheader("Cluster Distribution")
        cluster_data = {
            "Cluster": [f"Cluster {i}" for i in range(optimal_k)],
            "Count": [cluster_counts[i] for i in range(optimal_k)]
        }
        st.bar_chart(cluster_data, x="Cluster", y="Count")
        
        # Cluster details with category mapping
        st.subheader("Cluster Details")
        
        for cluster_id in range(optimal_k):
            cluster_cards = [card for card in cards_data if card['cluster'] == cluster_id]
            cluster_categories = [card['category'] for card in cluster_cards]
            category_distribution = Counter(cluster_categories)
            
            with st.expander(f"Cluster {cluster_id} - {len(cluster_cards)} cards"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Category Distribution:**")
                    for category, count in category_distribution.most_common():
                        st.write(f"- {category}: {count} cards")
                
                with col2:
                    if cluster_cards:
                        dominant_category = max(category_distribution, key=category_distribution.get)
                        st.metric("Dominant Category", dominant_category)
                        st.metric("Categories in Cluster", len(category_distribution))
        
        # Compare clusters with original categories
        st.subheader("Cluster vs Category Analysis")
        
        # Create a matrix showing cluster-category relationships
        cluster_category_matrix = []
        for cluster_id in range(optimal_k):
            cluster_cards = [card for card in cards_data if card['cluster'] == cluster_id]
            cluster_categories = Counter([card['category'] for card in cluster_cards])
            
            for category in set(categories):
                count = cluster_categories.get(category, 0)
                cluster_category_matrix.append({
                    'Cluster': f'Cluster {cluster_id}',
                    'Category': category,
                    'Count': count
                })
        
        # Display as a heatmap-like table
        import pandas as pd
        df_matrix = pd.DataFrame(cluster_category_matrix)
        pivot_table = df_matrix.pivot(index='Cluster', columns='Category', values='Count').fillna(0)
        
        st.write("**Cluster-Category Relationship Matrix:**")
        st.dataframe(pivot_table.style.background_gradient(cmap='Blues'), use_container_width=True)
        
        # Optional: Show detailed clustered card list
        with st.expander("Show Clustered Card Details"):
            for cluster_id in range(optimal_k):
                st.write(f"### Cluster {cluster_id}")
                cluster_cards = [card for card in cards_data if card['cluster'] == cluster_id]
                
                for card in cluster_cards:
                    st.write(f"**ID:** {card['id']} | **Category:** {card['category']} | **Cluster:** {card['cluster']}")
                    if 'question' in card['metadata']:
                        st.write(f"Question: {card['metadata']['question']}")
                    st.write("---")
    
    else:
        st.warning("No vector data available for clustering. Ensure 'include_values=True' in your query.")
        
except Exception as e:
    st.error(f"Error retrieving data from Pinecone: {str(e)}")
    st.info("Please check your Pinecone configuration and ensure the database contains flashcards with category metadata.")