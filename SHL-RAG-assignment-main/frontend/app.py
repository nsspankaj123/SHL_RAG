import streamlit as st
import requests

# Add custom CSS for improved UI with contrasting colors and color psychology
st.markdown("""
    <style>
        body {
            background-color: #f9f9f9;
            color: #333;
            font-family: 'Arial', sans-serif;
        }

        .title {
            font-size: 2.5rem;
            font-weight: bold;
            color: #2C3E50;  /* Deep Blue for professionalism and trust */
            text-align: center;
        }

        .button {
            background-color: #3498db;  /* Blue for trust and professionalism */
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 1.1rem;
            transition: background-color 0.3s ease;
        }

        .button:hover {
            background-color: #2980b9;  /* Slightly darker blue for hover effect */
        }

        .button-update {
            background-color: #2ecc71;  /* Green for success */
        }

        .button-update:hover {
            background-color: #27ae60;  /* Darker green for hover effect */
        }

        .card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            padding: 20px;
            transition: transform 0.3s ease-in-out;
            border-left: 5px solid #3498db;  /* Blue accent */
        }

        .card:hover {
            transform: scale(1.05);
        }

        .card-header {
            font-size: 1.4rem;
            font-weight: bold;
            color: #2980b9;  /* Deep Blue for titles */
        }

        .card-body {
            margin-top: 10px;
            color: #555;
        }

        .card-footer {
            text-align: right;
            margin-top: 15px;
        }

        .spinner {
            font-size: 1.5rem;
            color: #3498db;  /* Blue spinner for consistency */
        }

        .warning-text {
            color: #e74c3c;  /* Red for warning or errors */
            font-weight: bold;
        }

        .success-text {
            color: #2ecc71;  /* Green for success messages */
        }

        .highlight {
            color: #f39c12;  /* Orange for important highlights */
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Add a title with color psychology in mind
st.markdown('<div class="title">SHL Assessment Recommender</div>', unsafe_allow_html=True)

FASTAPI_URL = "https://shl-rag-assignment.onrender.com/"  # your deployed backend

if st.button("🔄 Update Assessment Data", key="update", help="Click to refresh the data from the backend", use_container_width=True):
    with st.spinner("Updating data..."):
        try:
            response = requests.post(f"{FASTAPI_URL}/update-data")
            if response.status_code == 200:
                st.success("✅ Data updated successfully!", icon="✅")
            else:
                st.error(f"❌ Failed to update: {response.status_code}", icon="⚠️")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}", icon="⚠️")

query = st.text_input("Enter job role or keywords:", help="Enter job role or keywords to search for relevant assessments")

if st.button("Search", key="search", help="Search assessments based on your query", use_container_width=True):
    with st.spinner("Fetching recommendations..."):
        response = requests.post(f"{FASTAPI_URL}/recommend", json={"query": query})

        if response.status_code == 200:
            results = response.json().get("results", [])
            if results:
                st.success("Results loaded!", icon="✅")
                for result in results:
                    # Using a card layout for each result
                    with st.container():
                        st.markdown(f"""
                            <div class="card">
                                <div class="card-header">{result.get('name', 'Untitled')}</div>
                                <div class="card-body">
                                    <p>{result.get("description", "No description available.")}</p>
                                    <p><strong>Duration:</strong> {result.get('duration')} minutes</p>
                                    <p><strong>Remote Support:</strong> {result.get('remote_support')}</p>
                                    <p><strong>Adaptive:</strong> {result.get('adaptive')}</p>
                                </div>
                                <div class="card-footer">
                                    <a href="{result.get('url')}" target="_blank" class="button">More Info</a>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.warning("No results found.", icon="⚠️")
        else:
            st.error("Something went wrong fetching data.", icon="⚠️")
