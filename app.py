"""
Streamlit Web Interface for Product Research Tool
Combines profit calculation and description generation
"""
import streamlit as st
import asyncio
import sys
from pathlib import Path

# Fix for event loop issues in Streamlit
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Import the core functions
from main_enhanced import analyze_product_profit, generate_product_description

# Page config
st.set_page_config(
    page_title="Product Research Tool",
    page_icon="🔍",
    layout="wide"
)

# Title
st.title("🔍 AI Product Research Tool")
st.markdown("**Powered by Tavily MCP + OpenAI**")

# Create tabs
tab1, tab2 = st.tabs(["💰 Profit Calculator", "✍️ Description Generator"])

# Tab 1: Profit Calculator
with tab1:
    st.header("Product Profit Calculator")
    st.markdown("Analyze profitability by comparing Amazon and AliExpress prices")
    
    product_name_profit = st.text_input(
        "Enter Product Name:",
        key="profit_input",
        placeholder="e.g., sunset lamp projector"
    )
    
    if st.button("🔍 Analyze Profitability", key="profit_btn"):
        if product_name_profit:
            with st.spinner("🔎 Searching Amazon and AliExpress prices..."):
                try:
                    result = asyncio.run(analyze_product_profit(product_name_profit))
                    
                    st.success("✅ Analysis Complete!")
                    
                    # Display result in a nice format
                    st.markdown("---")
                    st.markdown(result)
                    
                    # Show file saved location
                    output_file = Path("outputs") / f"{product_name_profit.replace(' ', '_').lower()}_analysis.md"
                    if output_file.exists():
                        st.info(f"📄 Full report saved to: `{output_file}`")
                        
                        # Download button
                        with open(output_file, 'r', encoding='utf-8') as f:
                            st.download_button(
                                label="📥 Download Report",
                                data=f.read(),
                                file_name=output_file.name,
                                mime="text/markdown"
                            )
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter a product name")

# Tab 2: Description Generator
with tab2:
    st.header("Product Description Generator")
    st.markdown("Generate SEO-optimized product descriptions using AI research")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        product_name_desc = st.text_input(
            "Enter Product Name:",
            key="desc_input",
            placeholder="e.g., wireless bluetooth earbuds"
        )
    
    with col2:
        product_url = st.text_input(
            "Product URL (Optional):",
            key="url_input",
            placeholder="https://amazon.com/..."
        )
    
    if st.button("✍️ Generate Descriptions", key="desc_btn"):
        if product_name_desc:
            with st.spinner("🔎 Researching product features and benefits..."):
                try:
                    result = asyncio.run(generate_product_description(product_name_desc, product_url))
                    
                    st.success("✅ Descriptions Generated!")
                    
                    # Display results in columns
                    st.markdown("---")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    # Parse the result to extract different versions
                    # For now, display the full result
                    st.markdown(result)
                    
                    # Show file saved location
                    output_file = Path("outputs") / f"{product_name_desc.replace(' ', '_').lower()}_descriptions.md"
                    if output_file.exists():
                        st.info(f"📄 Full descriptions saved to: `{output_file}`")
                        
                        # Download button
                        with open(output_file, 'r', encoding='utf-8') as f:
                            st.download_button(
                                label="📥 Download Descriptions",
                                data=f.read(),
                                file_name=output_file.name,
                                mime="text/markdown"
                            )
                    
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.warning("⚠️ Please enter a product name")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
    <p>Built with LangChain, Tavily MCP, and OpenAI | 
    <a href='https://github.com/yourusername/product-research-tool' target='_blank'>GitHub</a></p>
    </div>
    """,
    unsafe_allow_html=True
)