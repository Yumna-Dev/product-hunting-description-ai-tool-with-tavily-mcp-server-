"""
Enhanced Product Research Tool
Combines profit calculation and description generation
"""
import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

# Fix console encoding for Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Load environment variables
load_dotenv()

# System prompt for profit calculation
PROFIT_CALCULATOR_PROMPT = """You are a product profit calculator assistant that helps e-commerce sellers 
validate product profitability.

When analyzing a product:
1. Search for the product on Amazon to find retail prices
2. Search for the product on AliExpress to find supplier/wholesale prices
3. Calculate the profit margin using this formula:
   - Profit = Amazon Price - AliExpress Price - (Amazon Price × 0.30 for fees)
   - Margin % = (Profit / Amazon Price) × 100

4. Provide a verdict:
   - ✅ PROFITABLE: Margin > 30%
   - ⚠️ MARGINAL: Margin 15-30%
   - ❌ NOT PROFITABLE: Margin < 15%

5. Save the analysis to a markdown file in the outputs folder.

Always extract actual prices from search results. If you can't find exact prices, 
estimate based on similar products and note it in your analysis.

Format your final report as a clean markdown table with all metrics."""


# System prompt for description generation
DESCRIPTION_GENERATOR_PROMPT = """You are an expert product description writer that creates 
SEO-optimized, compelling product descriptions for e-commerce platforms.

When given a product:
1. Use web search to research the product thoroughly:
   - Key features and specifications
   - Benefits and use cases
   - Target audience
   - Competitor descriptions on Amazon/AliExpress
   - Customer pain points it solves

2. Generate THREE versions of descriptions:
   
   **SHORT VERSION (50-75 words):**
   - Perfect for product listings and quick overview
   - Focus on 3-5 key features
   - Include main benefit
   - End with subtle call-to-action
   
   **MEDIUM VERSION (150-200 words):**
   - Ideal for main product page
   - Detailed features in paragraph form
   - Emotional benefits
   - Why this product stands out
   - Strong call-to-action
   
   **LONG VERSION (300-400 words):**
   - Comprehensive SEO-optimized description
   - Multiple paragraphs covering all aspects
   - Include storytelling elements
   - Address customer objections
   - Natural keyword integration
   - Detailed specifications
   - Multiple calls-to-action

3. Format requirements:
   - Write in persuasive, engaging tone
   - Use power words and emotional triggers
   - Include bullet points for key features
   - Make it scannable and easy to read
   - Optimize for SEO naturally (don't force keywords)

4. Save all three versions to a markdown file in the outputs folder with clear section headers.

Make the descriptions compelling enough that customers want to buy immediately!"""


async def get_mcp_client():
    """Initialize and return MCP client with Tavily and Filesystem servers."""
    
    # Verify API keys
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not set in environment")
    if not os.getenv("MODEL"):
        raise ValueError("MODEL not set in environment")
    if not os.getenv("TAVILY_API_KEY"):
        raise ValueError("TAVILY_API_KEY not set in environment")
    
    # Setup output directory
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    
    # Build Tavily remote MCP URL
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    tavily_mcp_url = f"https://mcp.tavily.com/mcp/?tavilyApiKey={tavily_api_key}"
    
    # Create MCP client
    client = MultiServerMCPClient(
        {
            "tavily": {
                "url": tavily_mcp_url,
                "transport": "http",
            },
            "filesystem": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    str(output_dir),
                ],
                "transport": "stdio",
            },
        }
    )
    
    return client, output_dir


async def analyze_product_profit(product_name: str):
    """Analyze a product for profitability."""
    
    # Initialize LLM
    model = os.getenv("MODEL")
    llm = ChatOpenAI(model=model, temperature=0)
    
    # Get MCP client
    client, output_dir = await get_mcp_client()
    
    # Get tools from MCP servers
    print("Connecting to MCP servers...")
    tools = await client.get_tools()
    print(f"Connected! Available tools: {[tool.name for tool in tools]}")
    
    # Create the agent
    agent = create_agent(
        llm,
        tools,
        system_prompt=PROFIT_CALCULATOR_PROMPT,
    )
    
    # Build the query
    query = f"""Analyze the product: "{product_name}"

Steps to follow:
1. Search for "{product_name} Amazon price" to find Amazon retail prices
2. Search for "{product_name} AliExpress supplier price" to find wholesale prices
3. Calculate profit margin (remember to subtract 30% fees from Amazon price)
4. Create a detailed markdown analysis report
5. Save the report to a file named "{product_name.replace(' ', '_').lower()}_analysis.md"

Provide your complete analysis with a clear PROFITABLE/NOT PROFITABLE verdict."""

    print(f"\nAnalyzing product: {product_name}")
    print("=" * 50)

    # Run the agent
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": query}]}
    )

    # Extract and return the final response
    final_message = response["messages"][-1].content
    print("\nANALYSIS RESULT:")
    print("=" * 50)
    print(final_message)
    
    return final_message


async def generate_product_description(product_name: str, product_url: str = None):
    """Generate product descriptions using AI research."""
    
    # Initialize LLM
    model = os.getenv("MODEL")
    llm = ChatOpenAI(model=model, temperature=0.7)  # Higher temp for creative writing
    
    # Get MCP client
    client, output_dir = await get_mcp_client()
    
    # Get tools from MCP servers
    print("Connecting to MCP servers...")
    tools = await client.get_tools()
    print(f"Connected! Available tools: {[tool.name for tool in tools]}")
    
    # Create the agent
    agent = create_agent(
        llm,
        tools,
        system_prompt=DESCRIPTION_GENERATOR_PROMPT,
    )
    
    # Build the query
    url_context = f"\nProduct URL: {product_url}" if product_url else ""
    
    query = f"""Generate compelling product descriptions for: "{product_name}"{url_context}

Steps to follow:
1. Search for "{product_name} features specifications benefits"
2. Search for "{product_name} Amazon product description"
3. Research the target audience and their needs
4. Generate THREE versions of descriptions:
   - SHORT (50-75 words) - for listings
   - MEDIUM (150-200 words) - for product pages
   - LONG (300-400 words) - SEO-optimized detailed description
5. Include relevant bullet points for key features
6. Save all versions to a file named "{product_name.replace(' ', '_').lower()}_descriptions.md"

Make the descriptions persuasive, benefit-focused, and ready to copy-paste!"""

    print(f"\nGenerating descriptions for: {product_name}")
    print("=" * 50)

    # Run the agent
    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": query}]}
    )

    # Extract and return the final response
    final_message = response["messages"][-1].content
    print("\nDESCRIPTIONS GENERATED:")
    print("=" * 50)
    print(final_message)
    
    return final_message


async def main():
    """Main entry point for testing."""
    print("\n" + "=" * 50)
    print("PRODUCT RESEARCH TOOL - ENHANCED")
    print("=" * 50)
    
    # Test profit calculation
    print("\n[TEST 1: PROFIT CALCULATOR]")
    await analyze_product_profit("sunset lamp projector")
    
    print("\n\n")
    
    # Test description generation
    print("[TEST 2: DESCRIPTION GENERATOR]")
    await generate_product_description("wireless bluetooth earbuds")


if __name__ == "__main__":
    asyncio.run(main())