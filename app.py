import streamlit as st
from groq import Groq
import requests
import json

st.set_page_config(page_title="RZ Creative Shop - SEO & WooCommerce Tool", layout="wide")

st.title("🚀 RZ Creative Shop: AI SEO & WooCommerce Manager")
st.markdown("Powered by **Groq AI (Llama-3.3-70b)** & **WooCommerce REST API**")

# Sidebar for API Keys
st.sidebar.header("🔑 Configuration")
groq_api_key = st.sidebar.text_input("Groq API Key", type="password")

st.sidebar.markdown("---")
st.sidebar.header("🛒 WooCommerce Store Settings")
wc_url = st.sidebar.text_input("Store URL (e.g., https://rzcreativeshop.com)")
wc_consumer_key = st.sidebar.text_input("Consumer Key", type="password")
wc_consumer_secret = st.sidebar.text_input("Consumer Secret", type="password")

# Main Tabs
tab1, tab2 = st.tabs(["✨ AI SEO Generator", "📦 WooCommerce Product Push"])

with tab1:
    st.subheader("Generate SEO Optimized Content for Products")
    product_name = st.text_input("Product Name / Raw Description")
    keywords = st.text_input("Target Keywords (comma separated)")

    if st.button("Generate SEO Content"):
        if not groq_api_key:
            st.error("Please enter your Groq API Key in the sidebar.")
        elif not product_name:
            st.warning("Please enter a product name.")
        else:
            try:
                client = Groq(api_key=groq_api_key)
                prompt = f"""
                You are an expert E-commerce SEO copywriter. Generate the following for the product: '{product_name}' targeting keywords: '{keywords}'.
                Provide the response in clear sections:
                1. SEO Optimized Title (Max 60 chars)
                2. Meta Description (Max 160 chars)
                3. Engaging Product Description (HTML formatted for WooCommerce)
                4. Backend Tags/Keywords
                """
                
                with st.spinner("Generating content with Groq AI..."):
                    chat_completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7,
                    )
                    result = chat_completion.choices[0].message.content
                    st.success("SEO Content Generated Successfully!")
                    st.markdown(result)
            except Exception as e:
                st.error(f"Error: {e}")

with tab2:
    st.subheader("Push Product to WooCommerce")
    p_name = st.text_input("Product Title")
    p_price = st.text_input("Regular Price")
    p_desc = st.text_area("Product Description")

    if st.button("Publish to WooCommerce"):
        if not wc_url or not wc_consumer_key or not wc_consumer_secret:
            st.error("Please provide all WooCommerce API credentials in the sidebar.")
        else:
            url = f"{wc_url.rstrip('/')}/wp-json/wc/v3/products"
            data = {
                "name": p_name,
                "regular_price": p_price,
                "description": p_desc,
                "status": "publish"
            }
            try:
                response = requests.post(
                    url,
                    json=data,
                    auth=(wc_consumer_key, wc_consumer_secret)
                )
                if response.status_code == 201:
                    st.success("Product successfully published to WooCommerce!")
                    st.json(response.json())
                else:
                    st.error(f"Failed to publish: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")
