import streamlit as st
from groq import Groq
import requests
import json

st.set_page_config(page_title="RZ Creative Shop - Pro SEO & WooCommerce", layout="wide")

st.title("🚀 RZ Creative Shop: Professional WooCommerce Studio")
st.markdown("Powered by **Groq AI (Llama-3.3-70b)** & **WooCommerce REST API**")

# Sidebar Configuration
st.sidebar.header("🔑 API Credentials")
groq_api_key = st.sidebar.text_input("Groq API Key", type="password")

st.sidebar.markdown("---")
st.sidebar.header("🛒 WooCommerce Store")
wc_url = st.sidebar.text_input("Store URL", value="https://rzcreativeshop.com")
wc_consumer_key = st.sidebar.text_input("Consumer Key", type="password")
wc_consumer_secret = st.sidebar.text_input("Consumer Secret", type="password")

# Tabs
tab1, tab2 = st.tabs(["✨ AI SEO & Content Generator", "📦 Publish to WooCommerce (with Images)"])

with tab1:
    st.subheader("Generate SEO Content with Groq AI")
    product_name = st.text_input("Product Name / Raw Details")
    keywords = st.text_input("Focus Keywords (comma separated)")

    if st.button("Generate Optimized SEO Data"):
        if not groq_api_key:
            st.error("Please enter your Groq API Key.")
        elif not product_name:
            st.warning("Please enter a product name.")
        else:
            try:
                client = Groq(api_key=groq_api_key)
                prompt = f"""
                You are an expert E-commerce SEO Copywriter for RZ Creative Shop. Create SEO optimized content for: '{product_name}' targeting keywords: '{keywords}'.
                Provide in format:
                - SEO Title (Under 60 chars)
                - Meta Description (Under 160 chars)
                - HTML Product Description (Include <h2> subheadings and bullet points for features)
                """
                with st.spinner("Generating with Groq AI..."):
                    res = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7,
                    )
                    st.success("Generated Successfully!")
                    st.markdown(res.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")

with tab2:
    st.subheader("Push Product with Images & SEO Structure")
    p_name = st.text_input("Product Title", key="p_title")
    p_price = st.text_input("Regular Price ($)", key="p_price")
    p_desc = st.text_area("Product Description (HTML format with <h2>)", key="p_desc")
    
    # Image URLs input box
    st.markdown("### Product Images Setup")
    img_input = st.text_area("Paste Image URLs (Put each image link on a new line)")

    if st.button("Publish Product Now"):
        if not wc_url or not wc_consumer_key or not wc_consumer_secret:
            st.error("Please provide WooCommerce credentials in sidebar.")
        else:
            url = f"{wc_url.rstrip('/')}/wp-json/wc/v3/products"
            
            # Format image links into WooCommerce required JSON structure
            images_list = []
            if img_input:
                for line in img_input.split("\n"):
                    if line.strip():
                        images_list.append({"src": line.strip()})

            data = {
                "name": p_name,
                "regular_price": p_price,
                "description": p_desc,
                "images": images_list,
                "status": "publish"
            }
            
            try:
                response = requests.post(
                    url,
                    json=data,
                    auth=(wc_consumer_key, wc_consumer_secret)
                )
                if response.status_code == 201:
                    st.success("Product published successfully with images and SEO structure!")
                    st.json(response.json())
                else:
                    st.error(f"Failed: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")
