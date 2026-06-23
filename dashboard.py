import streamlit as st
import pandas as pd
from supabase import create_client
import os
from dotenv import load_dotenv
from research_module import tavily

# Configuration
load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))

st.set_page_config(layout="wide", page_title="ICM Inventory Command Center")

st.title("Inventory Command Center")

tab1, tab2 = st.tabs(["Inventory", "Manual Review Queue"])

# --- TAB 1: Inventory ---
with tab1:
    st.header("Cataloged Items")
    try:
        response = supabase.table("items").select("*").execute()
        df = pd.DataFrame(response.data)
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("No items cataloged yet.")
    except Exception as e:
        st.error(f"Failed to load inventory: {e}")

# --- TAB 2: Manual Review Queue ---
with tab2:
    st.header("Manual Review Required")
    # Fetch only unconfirmed items
    try:
        unconfirmed = supabase.table("items").select("*").eq("status", "manual_review_required").execute().data
    except Exception as e:
        st.error(f"Failed to load queue: {e}")
        unconfirmed = []
    
    if not unconfirmed:
        st.success("Queue clear! All items verified.")
    else:
        for item in unconfirmed:
            # Each expander uses a unique key based on the SKU
            with st.expander(f"Review: {item['sku']}", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Current Status**: {item['status']}")
                    st.write(f"**Draft Title**: {item['title']}")
                
                with col2:
                    # Dynamic Search Query with unique key
                    search_query = st.text_input(
                        f"Research Query for {item['sku']}", 
                        value=f"identify {item['title']} vintage furniture",
                        key=f"search_input_{item['sku']}"
                    )
                    
                    if st.button(f"Search Web for {item['sku']}", key=f"search_btn_{item['sku']}"):
                        with st.spinner("Consulting provenance database..."):
                            # Perform research via Tavily module
                            result = tavily.search(search_query)
                            
                            if result and 'results' in result and len(result['results']) > 0:
                                st.write("### Research Findings:")
                                st.write(result['results'][0]['content'])
                            else:
                                st.warning("No clear results found.")
                            
                    # Commit Logic with unique keys
                    new_title = st.text_input(f"Verified Title for {item['sku']}", value=item['title'], key=f"title_input_{item['sku']}")
                    if st.button(f"Commit {item['sku']} to Inventory", key=f"commit_btn_{item['sku']}"):
                        try:
                            supabase.table("items").update({
                                "title": new_title, 
                                "status": "draft"
                            }).eq("sku", item['sku']).execute()
                            st.success(f"Item {item['sku']} updated! Please refresh to clear from queue.")
                        except Exception as e:
                            st.error(f"Commit failed: {e}")