"""
Product Profit Calculator - Interactive CLI
Run this for an interactive product analysis experience.
Uses Tavily Remote MCP for web search (no local installation required).
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

load_dotenv()

SYSTEM_PROMPT = """You are a product profit calculator assistant for e-commerce sellers.

When analyzing a product:
1. Search for the product on Amazon to find retail prices
2. Search for the product on AliExpress to find supplier prices
3. Calculate profit margin:
   - Profit = Amazon Price - AliExpress Price - (Amazon Price × 0.30)
   - Margin % = (Profit / Amazon Price) × 100

4. Verdict:
   - ✅ PROFITABLE: Margin > 30%
   - ⚠️ MARGINAL: Margin 15-30%
   - ❌ NOT PROFITABLE: Margin < 15%

5. Save analysis to markdown file in outputs folder.

Always provide actual prices from search results. Format as clean markdown table."""


async def run_interactive():
    """Run interactive product analysis session."""
    
    # Check API keys
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not set")
        print("   Copy .env.example to .env and add your keys")
        return

    if not os.getenv("TAVILY_API_KEY"):
        print("Error: TAVILY_API_KEY not set")
        print("   Get free key at: https://tavily.com")
        return
    
    output_dir = Path(__file__).parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    
    # Build Tavily remote MCP URL
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    tavily_mcp_url = f"https://mcp.tavily.com/mcp/?tavilyApiKey={tavily_api_key}"
    
    print("\n" + "=" * 50)
    print("PRODUCT PROFIT CALCULATOR")
    print("=" * 50)
    print("Enter product names to analyze profitability.")
    print("Type 'quit' or 'exit' to stop.\n")
    
    model = os.getenv("MODEL", "gpt-4o")
    llm = ChatOpenAI(model=model, temperature=0)

    # Create MCP client - no context manager in newer versions
    client = MultiServerMCPClient(
        {
            # Tavily Remote MCP - no local installation needed!
            "tavily": {
                "url": tavily_mcp_url,
                "transport": "http",
            },
            # Local MCP filesystem server for saving reports
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", str(output_dir)],
                "transport": "stdio",
            },
        }
    )

    print("Connecting to MCP servers...")
    tools = await client.get_tools()
    print(f"Ready! Tools: {[t.name for t in tools]}\n")

    agent = create_agent(llm, tools, system_prompt=SYSTEM_PROMPT)
    
    while True:
        try:
            product = input("Enter product name: ").strip()

            if product.lower() in ["quit", "exit", "q"]:
                print("\nGoodbye!")
                break

            if not product:
                print("Please enter a product name\n")
                continue

            print(f"\nAnalyzing: {product}")
            print("-" * 40)
            
            query = f"""Analyze: "{product}"

1. Search for "{product} Amazon price"
2. Search for "{product} AliExpress price"
3. Calculate profit (subtract 30% fees)
4. Save report to "{product.replace(' ', '_').lower()}_analysis.md"

Give clear verdict: PROFITABLE or NOT PROFITABLE with reasoning."""

            response = await agent.ainvoke(
                {"messages": [{"role": "user", "content": query}]}
            )

            print("\nRESULT:")
            print("=" * 40)
            print(response["messages"][-1].content)
            print("\n")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    asyncio.run(run_interactive())