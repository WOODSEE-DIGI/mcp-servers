# MCP Servers Collection

A curated, sanitized set of MCP servers that run locally on macOS. No subscriptions required.

## What is this?

This repo contains a manifest (`servers.json`) and an install script (`install.py`) that clones, builds, and wires up a collection of local-first MCP servers.

## Quick install

```bash
git clone https://github.com/WOODSEE-DIGI/mcp-servers.git ~/GitHub/AI-ML-Agents/mcp-servers
cd ~/GitHub/AI-ML-Agents/mcp-servers
python3 install.py
```

## For OpenCode users

If a friend wants OpenCode to install this for them, they can paste this prompt:

> Clone https://github.com/WOODSEE-DIGI/mcp-servers.git and run install.py. Then load the generated MCP config from ~/.ai-context/mcp-registry/friends-mcp-config.json.

## Included servers

| Server | Purpose | Extra requirements |
|---|---|---|
| ai-context-bridge | Cross-project context, memory, builds | — |
| playwright-mcp | Browser automation | Playwright browsers |
| firecrawl-mcp | Web scrape/search/crawl | Local Firecrawl backend |
| webclaw-mcp | Fast local web scraping | Rust toolchain |
| crawlkit-mcp | CrawlKit API wrapper | CrawlKit backend |
| read-website-fast | Token-efficient page extraction | — |
| whatsapp-mcp | WhatsApp integration | whatsapp-bridge |
| qwen3-mcp-server | Local Qwen3/Ministral models | Ollama or LM Studio |
| swift-terminals | Persistent terminal sessions | — |
| xcodebuildmcp | Xcode build/simulator tools | Xcode |

## Notes

- All repos are cloned under `~/GitHub/AI-ML-Agents` by default.
- The install script generates `~/.ai-context/mcp-registry/friends-mcp-config.json`.
- Some servers need a backend running (Firecrawl, CrawlKit, Ollama, etc.). The install script builds the wrappers; you start the backends separately.

## License

Per-server licenses apply. Most are MIT or Apache-2.0. Firecrawl core is AGPL; the wrapper is MIT.
