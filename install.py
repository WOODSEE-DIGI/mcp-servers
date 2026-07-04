#!/usr/bin/env python3
"""Install MCP servers and their backends."""

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

MANIFEST = Path(__file__).parent / "servers.json"


def run(cmds, cwd=None, desc="", shell=True, check=True):
    """Run shell commands. Returns True if all succeed."""
    for cmd in cmds:
        if not cmd:
            continue
        print(f"\n▶ {desc or cwd or ''}: {cmd}")
        result = subprocess.run(cmd, shell=shell, cwd=cwd)
        if check and result.returncode != 0:
            print(f"✗ Failed: {cmd}")
            return False
    return True


def tool_available(name):
    return shutil.which(name) is not None


def clone_or_update(repo, local_path):
    if local_path.exists() and (local_path / ".git").exists():
        print(f"\n↻ Updating {local_path.name}")
        run(["git pull"], local_path, check=False)
    else:
        print(f"\n↓ Cloning {repo}")
        local_path.parent.mkdir(parents=True, exist_ok=True)
        run([f"git clone {repo} {local_path}"], local_path.parent)


def install_server(server):
    name = server["name"]
    repo = server["repo"]
    local_path = Path(server["local_path"]).expanduser()

    print(f"\n{'='*60}")
    print(f"MCP Server: {name}")
    print(f"{'='*60}")

    clone_or_update(repo, local_path)

    build = server.get("build", [])
    if build and not run(build, local_path, name):
        print(f"⚠ {name} build had issues")
        return False

    extras = server.get("extras", [])
    for extra in extras:
        run([extra], local_path, name, check=False)

    print(f"✓ {name} ready")
    return True


def wait_for_health(url, timeout=60):
    print(f"  Waiting for {url} ...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            urllib.request.urlopen(url, timeout=2)
            print(f"  ✓ {url} is up")
            return True
        except Exception:
            time.sleep(1)
    print(f"  ⚠ {url} did not respond within {timeout}s (may still be starting)")
    return False


def install_backend(backend):
    name = backend["name"]
    print(f"\n{'='*60}")
    print(f"Backend: {name}")
    print(f"{'='*60}")

    # Check required tools
    for need in backend.get("needs", []):
        if not tool_available(need):
            print(f"⚠ '{need}' is not installed. Skipping {name} backend.")
            print(f"   Install {need} and re-run to enable this backend.")
            return False

    repo = backend.get("repo")
    local_path = Path(backend["local_path"]).expanduser() if "local_path" in backend else None

    if repo and local_path:
        clone_or_update(repo, local_path)

    setup = backend.get("setup", [])
    if setup and not run(setup, local_path, name, check=False):
        print(f"⚠ {name} setup had issues")
        return False

    start = backend.get("start", [])
    if not start:
        print(f"✓ {name} prepared (no auto-start defined)")
        return True

    if backend.get("interactive"):
        print(f"\n🚀 To start {name}, run:")
        print(f"   cd {local_path}")
        for cmd in start:
            print(f"   {cmd}")
        print(f"   ({backend.get('note', '')})")
        return True

    if not run(start, local_path, name, check=False):
        print(f"⚠ {name} start had issues")
        return False

    health = backend.get("health_url")
    if health:
        wait_for_health(health)

    print(f"✓ {name} started")
    return True


def generate_mcp_config(servers):
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
    parser = argparse.ArgumentParser(description="Install MCP servers and backends")
    parser.add_argument("--no-backends", action="store_true", help="Skip backend setup")
    parser.add_argument("--backend", type=str, help="Install only one backend by name")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text())
    servers = manifest["servers"]
    backends = manifest.get("backends", [])

    # Install MCP servers
    server_failures = []
    for server in servers:
        try:
            if not install_server(server):
                server_failures.append(server["name"])
        except Exception as e:
            print(f"✗ {server['name']} failed: {e}")
            server_failures.append(server["name"])

    # Install backends
    backend_failures = []
    if not args.no_backends:
        for backend in backends:
            if args.backend and backend["name"] != args.backend:
                continue
            try:
                if not install_backend(backend):
                    backend_failures.append(backend["name"])
            except Exception as e:
                print(f"✗ {backend['name']} failed: {e}")
                backend_failures.append(backend["name"])

    config_path = generate_mcp_config(servers)

    print("\n" + "=" * 60)
    print("INSTALL SUMMARY")
    print("=" * 60)
    if server_failures:
        print(f"⚠ MCP servers with issues: {', '.join(server_failures)}")
    else:
        print("✓ All MCP servers installed")

    if not args.no_backends:
        if backend_failures:
            print(f"⚠ Backends with issues: {', '.join(backend_failures)}")
        else:
            print("✓ All backends started")

    print(f"\nMCP config: {config_path}")
    print("\nNext steps:")
    print("1. Copy relevant entries into your MCP client config.")
    print("2. For interactive backends (e.g. whatsapp-bridge), start them manually.")
    print("3. For missing tools (docker, go, etc.), install them and re-run.")


if __name__ == "__main__":
    main()
