import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="AWS Agreement Q&A",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AWS Customer Agreement Assistant")


if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("📊 Analytics Dashboard")
    if st.button("🔄 Refresh Analytics"):
        try:
            response = requests.get(f"{API_URL}/analytics")
            if response.status_code == 200:
                data = response.json()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Queries", data['total_queries'])
                with col2:
                    st.metric("No Answer Rate", f"{data['no_answer_rate']*100:.1f}%")
                with col3:
                    st.metric("Avg Response", f"{data['avg_response_latency_ms']}ms")
                
                st.subheader("🔝 Most Frequent Questions")
                df = pd.DataFrame(
                    data['most_frequent_queries'],
                    columns=['Question', 'Count']
                )
                st.dataframe(df, use_container_width=True)
            else:
                st.error("Failed to fetch analytics")
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to FastAPI backend. Is it running?")


st.subheader("💬 Ask a question about the AWS Customer Agreement")


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("📚 View Sources"):
                for i, source in enumerate(message["sources"], 1):
                    st.text(f"Source {i}:")
                    st.text(source['content'][:300] + "...")


if prompt := st.chat_input("e.g., What are the payment terms?"):
   
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Searching and generating answer..."):
            try:
                response = requests.post(
                    f"{API_URL}/ask",
                    json={"query": prompt, "top_k": 3}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data['found_answer']:
                        st.success("✅ Answer found in document")
                    else:
                        st.warning("⚠️ Answer not found in document")
                    
                    st.markdown(data['answer'])
                    
                    with st.expander("📚 View Sources"):
                        for i, source in enumerate(data['sources'], 1):
                            st.text(f"Source {i}:")
                            st.text(source['content'][:300] + "...")
                            st.text(f"Page: {source['metadata'].get('page', 'N/A')}")
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": data['answer'],
                        "sources": data['sources']
                    })
                else:
                    st.error(f"Error: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to FastAPI backend. Please start the server.")

if st.sidebar.button("🔍 Check Health"):
    try:
        response = requests.get(f"{API_URL}/health")
        if response.status_code == 200:
            st.sidebar.success("✅ Backend is healthy")
        else:
            st.sidebar.error("❌ Backend is unhealthy")
    except:
        st.sidebar.error("❌ Cannot connect to backend")