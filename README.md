# MCP Servers Collection

A curated, sanitized set of MCP servers that run locally on macOS. No subscriptions required.

## Quick install

```bash
git clone https://github.com/WOODSEE-DIGI/mcp-servers.git ~/GitHub/AI-ML-Agents/mcp-servers
cd ~/GitHub/AI-ML-Agents/mcp-servers
python3 install.py
```

This installs all MCP server wrappers **and** starts the local backends where possible.

## For OpenCode users

Paste this prompt:

> Clone https://github.com/WOODSEE-DIGI/mcp-servers.git and run `python3 install.py`. Then load the generated MCP config from `~/.ai-context/mcp-registry/friends-mcp-config.json`.

## What gets installed

### MCP servers

| Server | Purpose |
|---|---|
| ai-context-bridge | Cross-project context, memory, builds |
| playwright-mcp | Browser automation |
| firecrawl-mcp | Web scrape/search/crawl |
| webclaw-mcp | Fast local web scraping |
| crawlkit-mcp | CrawlKit API wrapper |
| read-website-fast | Token-efficient page extraction |
| whatsapp-mcp | WhatsApp integration |
| qwen3-mcp-server | Local Qwen3/Ministral models |
| swift-terminals | Persistent terminal sessions |
| xcodebuildmcp | Xcode build/simulator tools |

### Backends (auto-started if dependencies are present)

| Backend | Requirement | What the script does |
|---|---|---|
| firecrawl-backend | Docker | Clones Firecrawl, writes `.env`, runs `docker compose up -d` |
| crawlkit-backend | Docker | Builds CrawlKit Docker image, runs on `:8088` |
| ollama | — | Installs Ollama, starts it, pulls `qwen3:8b` |
| whatsapp-bridge | Go | Builds the bridge; you start it manually and scan the QR code |
| Playwright browsers | — | `npx playwright install chromium` |

## Manual requirements

The script cannot install these for you:

- **Docker** — for Firecrawl and CrawlKit backends
- **Go** — for the WhatsApp bridge
- **Xcode** — for XcodeBuildMCP
- **uv** — for the WhatsApp MCP Python server (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

If a dependency is missing, the script skips that backend and tells you.

## Options

```bash
# Skip all backends
python3 install.py --no-backends

# Install only one backend
python3 install.py --backend ollama
```

## License

Per-server licenses apply.
