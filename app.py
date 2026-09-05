import streamlit as st
from groq import Groq
import requests
import json

st.set_page_config(page_title="RZ Creative Shop - Advanced Studio", layout="wide")

st.title("🚀 RZ Creative Shop: Advanced AI SEO & Multi-Image Manager")
st.markdown("Powered by **Groq AI (Llama-3.3-70b)** & **WooCommerce REST API**")

# Sidebar for API Keys & Store Config
st.sidebar.header("🔑 API Configuration")
groq_api_key = st.sidebar.text_input("Groq API Key", type="password")

st.sidebar.markdown("---")
st.sidebar.header("🛒 WooCommerce Store Settings")
wc_url = st.sidebar.text_input("Store URL (e.g., https://rzcreativeshop.com)")
wc_consumer_key = st.sidebar.text_input("Consumer Key", type="password")
wc_consumer_secret = st.sidebar.text_input("Consumer Secret", type="password")

# Main Tabs for Advanced Features
tab1, tab2, tab3 = st.tabs(["✨ AI SEO & Storyboard", "🎨 Creative Visual & Reference Images", "📦 Advanced WooCommerce Push"])

with tab1:
    st.subheader("Generate Advanced SEO Content & Ad Copy")
    product_name = st.text_input("Product Name / Raw Description")
    keywords = st.text_input("Target Keywords (comma separated)")
    target_platform = st.selectbox("Platform", ["WooCommerce Store", "TikTok Ads (9:16)", "Shopify Store"])

    if st.button("Generate Professional Content"):
        if not groq_api_key:
            st.error("Please enter your Groq API Key in the sidebar.")
        elif not product_name:
            st.warning("Please enter a product name.")
        else:
            try:
                client = Groq(api_key=groq_api_key)
                prompt = f"""
                You are an expert E-commerce manager and creative director at RZ Creative Shop. 
                Generate professional content for: '{product_name}' targeting keywords: '{keywords}' for platform: '{target_platform}'.
                Provide clear sections:
                1. SEO Optimized Title
                2. Meta Description
                3. Engaging HTML Product Description (Formatted for E-commerce)
                4. Backend Tags/Keywords
                5. Short-form Video/Ad Hook Script (9:16 vertical format concept)
                """
                
                with st.spinner("Generating with Groq AI..."):
                    chat_completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7,
                    )
                    st.success("Content Generated Successfully!")
                    st.markdown(chat_completion.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")

with tab2:
    st.subheader("🎨 Creative Reference & Character Image Prompts")
    st.markdown("Generate multi-scene image prompts, banner layouts, and character concepts for your products.")
    
    img_concept_type = st.selectbox("Select Visual Type", ["Product Banner & Studio Setup", "Character / Avatar Ad Concept", "Reference Moodboard"])
    brand_style = st.text_input("Brand Vibe / Aesthetic (e.g., Minimalist, Vibrant 3D Cartoon, Luxury Gold)")

    if st.button("Generate Visual Prompts"):
        if not groq_api_key:
            st.error("Please enter your Groq API Key.")
        else:
            try:
                client = Groq(api_key=groq_api_key)
                img_prompt = f"""
                Create 3 detailed AI image generation prompts (for Midjourney/DALL-E) for RZ Creative Shop.
                Type: {img_concept_type}
                Product/Theme: {product_name if 'product_name' in locals() and product_name else 'RZ Creative Shop Product'}
                Style/Vibe: {brand_style}
                Provide precise visual details, lighting, angles, and color schemes.
                """
                with st.spinner("Creating visual concepts..."):
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "user", "content": img_prompt}],
                    )
                    st.success("Visual Prompts Created!")
                    st.markdown(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error: {e}")

with tab3:
    st.subheader("📦 Advanced WooCommerce Push (Multi-Image Support)")
    p_name = st.text_input("Product Title", key="wc_title")
    p_price = st.text_input("Regular Price", key="wc_price")
    p_desc = st.text_area("Product Description (HTML supported)", key="wc_desc")
    
    # Multiple image URLs input for WooCommerce gallery
    st.markdown("### Product Images")
    img_urls_input = st.text_area("Image URLs (Enter each image URL on a new line)")

    if st.button("Publish Product with Images"):
        if not wc_url or not wc_consumer_key or not wc_consumer_secret:
            st.error("Please provide all WooCommerce API credentials in the sidebar.")
        else:
            url = f"{wc_url.rstrip('/')}/wp-json/wc/v3/products"
            
            # Format images list for WooCommerce API
            images_list = []
            if img_urls_input:
                urls = img_urls_input.split("\n")
                for u in urls:
                    if u.strip():
                        images_list.append({"src": u.strip()})

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
                    st.success("Product successfully published to WooCommerce with images!")
                    st.json(response.json())
                else:
                    st.error(f"Failed to publish: {response.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")
