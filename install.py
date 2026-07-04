#!/usr/bin/env python3
"""Install all MCP servers from the manifest."""

import json
import os
import subprocess
import sys
from pathlib import Path

MANIFEST = Path(__file__).parent / "servers.json"


def run(cmds, cwd, desc=""):
    """Run a list of shell commands in cwd."""
    for cmd in cmds:
        if not cmd:
            continue
        print(f"\n▶ {desc or cwd}: {cmd}")
        result = subprocess.run(cmd, shell=True, cwd=cwd)
        if result.returncode != 0:
            print(f"✗ Command failed: {cmd}")
            return False
    return True


def clone_or_update(repo, local_path):
    """Clone repo if missing, otherwise pull latest."""
    if local_path.exists() and (local_path / ".git").exists():
        print(f"\n↻ Updating {local_path.name}")
        run(["git pull"], local_path)
    else:
        print(f"\n↓ Cloning {repo} into {local_path}")
        local_path.parent.mkdir(parents=True, exist_ok=True)
        run([f"git clone {repo} {local_path}"], local_path.parent)


def install_server(server):
    """Clone, build, and verify one server."""
    name = server["name"]
    repo = server["repo"]
    local_path = Path(server["local_path"]).expanduser()

    print(f"\n{'='*60}")
    print(f"Installing {name}")
    print(f"{'='*60}")

    clone_or_update(repo, local_path)

    build = server.get("build", [])
    if build:
        if not run(build, local_path, name):
            print(f"⚠ {name} build had issues; continuing...")
            return False

    print(f"✓ {name} ready at {local_path}")
    return True


def generate_mcp_config(servers):
    """Generate a generic MCP client config."""
    mcp_servers = {}
    for s in servers:
        args = [str(Path(a).expanduser()) for a in s.get("args", [])]
        entry = {
            "command": str(Path(s["command"]).expanduser()),
            "args": args,
        }
        if "env" in s:
            entry["env"] = s["env"]
        mcp_servers[s["name"]] = entry

    config = {"mcpServers": mcp_servers}
    config_dir = Path.home() / ".ai-context" / "mcp-registry"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / "friends-mcp-config.json"
    config_path.write_text(json.dumps(config, indent=2))
    print(f"\n📝 Generated MCP config: {config_path}")
    return config_path


def main():
    manifest = json.loads(MANIFEST.read_text())
    servers = manifest["servers"]

    failures = []
    for server in servers:
        try:
            if not install_server(server):
                failures.append(server["name"])
        except Exception as e:
            print(f"✗ {server['name']} failed: {e}")
            failures.append(server["name"])

    config_path = generate_mcp_config(servers)

    print("\n" + "=" * 60)
    print("INSTALL SUMMARY")
    print("=" * 60)
    if failures:
        print(f"⚠ These servers had issues: {', '.join(failures)}")
    else:
        print("✓ All servers installed")
    print(f"\nMCP config written to: {config_path}")
    print("\nNext steps:")
    print("1. Review the generated config")
    print("2. Copy relevant entries into your MCP client config (Warp, OpenCode, Claude Code, etc.)")
    print("3. Start any required backends (Ollama, Firecrawl, CrawlKit, etc.)")
    print("\nFor OpenCode: point it at ~/.ai-context/mcp-registry/friends-mcp-config.json")


if __name__ == "__main__":
    main()
