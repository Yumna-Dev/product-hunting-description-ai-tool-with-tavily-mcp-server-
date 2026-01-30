# Product Profit Calculator - MVP

An AI-powered tool that validates e-commerce product profitability by comparing prices across Amazon and AliExpress using MCP (Model Context Protocol) servers.

**Features Tavily Remote MCP** - No local MCP server installation required for search!

## TL;DR - Quick Start

```bash
# 1. Install prerequisites (if needed)
# Python 3.11+, uv, Node.js 18+

# 2. Install dependencies
uv sync

# 3. Set up environment
cp .env.example .env
# Edit .env with your OPENAI_API_KEY, MODEL, and TAVILY_API_KEY

# 4. Run
uv run python main.py          # Single product
# OR
uv run python cli.py           # Interactive mode
```

Get API keys: [OpenAI](https://platform.openai.com/api-keys) | [Tavily (free)](https://tavily.com)

## What It Does

```
You: "Is 'sunset lamp projector' profitable?"

Agent: Connects to Tavily (remote) and Filesystem (local) MCP servers
1. Searches Amazon for retail price (via Tavily)
2. Searches AliExpress for supplier price (via Tavily)
3. Calculates profit margin (minus 30% fees)
4. Saves detailed report to file
5. Returns: PROFITABLE / NOT PROFITABLE
```

## Expected Output

When you run the calculator, you'll see:

```
==================================================
PRODUCT PROFIT CALCULATOR - MVP
==================================================
Connecting to MCP servers...
Connected! Available tools: ['tavily_search', 'tavily_extract', ...]

Analyzing product: sunset lamp projector
==================================================

ANALYSIS RESULT:
==================================================
I searched Amazon and AliExpress and saved the full analysis to
outputs/sunset_lamp_projector_analysis.md. Summary below.

Analysis (product: "sunset lamp projector")

- Amazon retail price: $15.99
- AliExpress supplier price: $0.99
- Amazon fee (30%): $4.80
- Profit: $10.20
- Margin %: 63.8%

Verdict: PROFITABLE (Margin > 30%)
```

**Generated Report** (`outputs/sunset_lamp_projector_analysis.md`):
```markdown
# Sunset Lamp Projector — Profitability Analysis

| Metric | Value |
|---|---:|
| Amazon retail price | $15.99 |
| AliExpress supplier price | $0.99 |
| Amazon fee (30%) | $4.80 |
| Profit | $10.20 |
| Margin | 63.8% |
| Verdict | PROFITABLE (Margin > 30%) |

Sources:
- Amazon: https://www.amazon.com/...
- AliExpress: https://inbusiness.aliexpress.com/...
```

## MCP Servers Used

| Server | Type | Purpose |
|--------|------|---------|
| **Tavily** | Remote | Web search for product prices (no local setup!) |
| **Filesystem** | Local | Save analysis reports |

## Prerequisites

- Python 3.11+ (Python 3.12 recommended)
- [uv](https://docs.astral.sh/uv/) package manager
- Node.js 18+ (for local Filesystem MCP server)
- OpenAI API key
- Tavily API key (free tier: 1000 searches/month)

## Quick Start from Scratch

Follow these steps to set up and run the project in a new folder:

### Step-by-Step Setup

#### 1. Install Prerequisites

**Install uv (if not installed):**
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Install Node.js (if not installed):**
- Download from [nodejs.org](https://nodejs.org/) (LTS version recommended)
- Or use package manager:
  ```bash
  brew install node        # macOS
  sudo apt install nodejs  # Ubuntu/Debian
  choco install nodejs     # Windows (with Chocolatey)
  ```

#### 2. Clone or Download Project

**Option A: Clone from Git (if available)**
```bash
git clone <repository-url>
cd mcp-profit-calculator2
```

**Option B: Create Project Manually**
```bash
mkdir product-profit-calculator
cd product-profit-calculator
# Download all project files into this directory
# OR copy files from the source location
```

#### 3. Install Python Dependencies

```bash
# This will create a virtual environment and install all dependencies
uv sync
```

**What this does:**
- Creates a `.venv` virtual environment
- Installs `langchain`, `langchain-openai`, `langchain-mcp-adapters`, and other dependencies
- Uses `pyproject.toml` for dependency management

#### 4. Get API Keys

**OpenAI API Key:**
1. Visit [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign in or create account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-proj-...`)
5. Save it securely (you won't see it again)

**Tavily API Key (FREE - 1000 searches/month):**
1. Visit [tavily.com](https://tavily.com)
2. Sign up for free account
3. Navigate to API Keys section
4. Copy your API key (starts with `tvly-...`)

#### 5. Configure Environment Variables

**Create `.env` file:**
```bash
# Copy the example file
cp .env.example .env

# Windows (Command Prompt)
copy .env.example .env
```

**Edit `.env` file** with your actual API keys:
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
MODEL=gpt-4o-mini
TAVILY_API_KEY=tvly-xxxxxxxxxxxxx
```

**Model Options:**
- `gpt-4o-mini` - Fastest and cheapest (~$0.001/analysis) - **Recommended for testing**
- `gpt-4o` - Balanced performance (~$0.01-0.03/analysis)
- `gpt-4-turbo` - Most capable but slower and expensive

#### 6. Run the Calculator

**Test with Single Product Analysis:**
```bash
uv run python main.py
```

This will analyze "sunset lamp projector" and save results to `outputs/` folder.

**Run Interactive CLI:**
```bash
uv run python cli.py
```

Then enter product names interactively:
```
Enter product name: wireless earbuds
Enter product name: portable blender
Enter product name: quit
```

## First Run Checklist

Before running the calculator, verify your setup:

- [ ] Python 3.11+ installed: `python --version` or `python3 --version`
- [ ] uv installed: `uv --version`
- [ ] Node.js installed: `node --version` (should show v18+)
- [ ] Project dependencies installed: `.venv` folder exists after `uv sync`
- [ ] `.env` file created and populated with valid API keys
- [ ] All three environment variables set: `OPENAI_API_KEY`, `MODEL`, `TAVILY_API_KEY`

**Quick validation command:**
```bash
# Check if all required tools are available
python --version && uv --version && node --version && echo "All tools installed!"

# Check if .env file exists
cat .env  # Linux/macOS
type .env  # Windows
```

If everything checks out, proceed to run the calculator!

## Usage Examples

### Interactive Mode
```
==================================================
PRODUCT PROFIT CALCULATOR
==================================================
Enter product names to analyze profitability.
Type 'quit' to stop.

Enter product name: led cloud light
Analyzing: led cloud light
------------------------------------------

RESULT:
==========================================
## Product Analysis: LED Cloud Light

| Metric | Value |
|--------|-------|
| Amazon Price | $29.99 |
| AliExpress Price | $8.20 |
| Fees (30%) | $9.00 |
| **Profit** | **$12.79** |
| **Margin** | **42.6%** |

VERDICT: PROFITABLE

Enter product name: quit
Goodbye!
```

### Modify main.py for Different Products

```python
# In main.py, change the products list:
products = [
    "sunset lamp projector",
    "portable blender",
    "led strip lights",
]
```

## Project Structure

```
product-profit-calculator/
├── main.py              # Single product analysis script
├── cli.py               # Interactive CLI script
├── pyproject.toml       # Python dependencies (required)
├── uv.lock              # Lock file for reproducible builds (auto-generated)
├── .env.example         # Environment variable template (required)
├── .env                 # Your actual API keys (you create this)
├── README.md            # Documentation (this file)
├── .venv/               # Virtual environment (auto-created by uv sync)
└── outputs/             # Analysis reports (auto-created on first run)
    └── *.md             # Product analysis markdown files
```

**Required Files to Start:**
- `main.py` - Main script
- `cli.py` - Interactive script
- `pyproject.toml` - Dependency configuration
- `.env.example` - Template for environment variables

**Files You Create:**
- `.env` - Copy from `.env.example` and add your API keys

**Auto-Generated:**
- `.venv/` - Created by `uv sync`
- `uv.lock` - Created by `uv sync`
- `outputs/` - Created on first run

## How It Works

```
┌─────────────────────────────────────┐
│         LangChain Agent             │
│    (Configurable Model + Tools)     │
└─────────────────┬───────────────────┘
                  │
       ┌──────────┴──────────┐
       ▼                     ▼
  ┌─────────┐          ┌──────────┐
  │ Tavily  │          │Filesystem│
  │ (Remote)│          │ (Local)  │
  └────┬────┘          └────┬─────┘
       │                    │
       ▼                    ▼
   Web Search             Save
   (No Setup!)          Reports
```

## Profit Calculation Formula

```
Amazon Price:     $25.00
AliExpress Price: $7.00
Fees (30%):       $7.50  (shipping, platform fees, etc.)
─────────────────────────
Profit:           $10.50
Margin:           42%    ($10.50 / $25.00)
```

### Verdict Thresholds

| Margin | Verdict |
|--------|---------|
| > 30% | PROFITABLE |
| 15-30% | MARGINAL |
| < 15% | NOT PROFITABLE |

## Why Tavily Remote MCP?

| Benefit | Description |
|---------|-------------|
| **No Local Setup** | Connects directly to `mcp.tavily.com` - no npx/npm needed for search |
| **Free Tier** | 1000 searches/month free |
| **AI-Optimized** | Results are optimized for LLM consumption |
| **Fast** | Direct HTTP connection, no subprocess overhead |

## Troubleshooting

### "OPENAI_API_KEY not set" or "MODEL not set"
```bash
# Make sure .env file exists and contains your keys
cat .env  # Linux/macOS
type .env  # Windows

# Should show:
# OPENAI_API_KEY=sk-...
# MODEL=gpt-4o
# TAVILY_API_KEY=tvly-...
```

### "TAVILY_API_KEY not set"
```bash
# Get free key at https://tavily.com
# Add to .env file
```

### "npx: command not found"
```bash
# Install Node.js from https://nodejs.org/
# Or via package manager:
brew install node        # macOS
sudo apt install nodejs  # Ubuntu
choco install nodejs     # Windows (with Chocolatey)
```

Note: npx is only needed for the Filesystem server (local), not for Tavily (remote).

### Connection Timeout to Tavily
```bash
# Check your internet connection
# Verify API key is correct
# Try: curl https://mcp.tavily.com/mcp/?tavilyApiKey=YOUR_KEY
```

### Unicode/Encoding Errors (Windows)
The script automatically handles UTF-8 encoding for Windows console. If you still see encoding issues, try:
```bash
# Run in Windows Terminal (recommended) instead of Command Prompt
# Or set console to UTF-8:
chcp 65001
```

### "BaseModel.__init__() takes 1 positional argument"
This error has been fixed. Make sure you're using the latest version of the code where `ChatOpenAI` is initialized with `model=model` (keyword argument).

### First Time Running - What to Expect

**Normal startup messages:**
```
Connecting to MCP servers...
Secure MCP Filesystem Server running on stdio
Client does not support MCP Roots, using allowed directories...
Connected! Available tools: [...]
```

These messages are normal! The filesystem server runs locally via npx and will show these informational messages.

**Timing:**
- First run: 10-30 seconds (MCP servers initialize, npm packages download)
- Subsequent runs: 5-15 seconds (faster, packages cached)
- Each product analysis: 10-20 seconds (depends on search complexity)

## Extending the MVP

Want to add more features? Here are ideas:

1. **Add Trends Analysis**: Add the Trends MCP server to find viral products
2. **Track Products Over Time**: Use Memory MCP to save and compare historical data
3. **Scrape More Platforms**: Add Apify MCP for eBay, Walmart, etc.
4. **Bulk Analysis**: Process CSV files of products

## API Costs

| Service | Free Tier | Cost per Analysis |
|---------|-----------|-------------------|
| Tavily | 1000 searches/month free | $0 (within free tier) |
| OpenAI gpt-4o | Pay-per-use | ~$0.01-0.03 |
| OpenAI gpt-4o-mini | Pay-per-use | ~$0.001-0.005 (cheaper) |

**Tip:** Start with `gpt-4o-mini` in your `.env` file to reduce costs during testing.

## License

MIT License - Use freely for personal or commercial projects.

## Credits

Built with:
- [LangChain](https://python.langchain.com/) - AI agent framework
- [MCP](https://modelcontextprotocol.io/) - Model Context Protocol
- [OpenAI](https://openai.com/) - GPT-4o language model
- [Tavily](https://tavily.com/) - AI-powered search API (Remote MCP)
"# product-hunting-description-ai-tool-with-tavily-mcp-server-" 
