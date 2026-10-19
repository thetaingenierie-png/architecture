#!/usr/bin/env python3
"""Installe les connecteurs Theta dans Claude, sur Mac ou Windows.

Le script ajoute les serveurs sans retirer ceux qui existent déjà.
"""
import json
import os
import shutil
import sys
from pathlib import Path

HELP_URL = "https://developer.api.autodesk.com/knowledge/public/v1/mcp"
FUSION_URL = "https://developer.api.autodesk.com/fusion/mcp"
REVIT_EXE = Path(
    r"C:\Program Files\Autodesk\Revit 2027 MCP Server Read-Tools Technical Preview"
) / "Autodesk.RevitMcpServer.Stdio.exe"


def tool(name):
    found = shutil.which(name)
    if found:
        return found
    home = Path.home()
    for candidate in (
        home / ".local" / "bin" / name,
        Path("/usr/local/bin") / name,
        Path("/opt/homebrew/bin") / name,
    ):
        if candidate.exists():
            return str(candidate)
    return name


def path_env():
    home = Path.home()
    parts = []
    for candidate in (home / ".local" / "bin", Path("/usr/local/bin"), Path("/opt/homebrew/bin")):
        if candidate.exists():
            parts.append(str(candidate))
    current = os.environ.get("PATH", "")
    if current:
        parts.append(current)
    return os.pathsep.join(parts)


def desktop_config():
    if sys.platform == "darwin":
        return Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        if not appdata:
            raise SystemExit("APPDATA est introuvable.")
        return Path(appdata) / "Claude" / "claude_desktop_config.json"
    return Path.home() / ".config/Claude/claude_desktop_config.json"


def load_json(path):
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def desktop_servers():
    npx = tool("npx")
    uvx = tool("uvx")
    env = {"PATH": path_env()}
    servers = {
        "autodesk-product-help": {
            "command": npx,
            "args": ["-y", "mcp-remote", HELP_URL],
            "env": env,
        },
        "autodesk-fusion-data": {
            "command": npx,
            "args": ["-y", "mcp-remote", FUSION_URL],
            "env": env,
        },
        "autocad": {
            "command": uvx,
            "args": ["--from", "autocad-mcp-pro", "autocad-mcp"],
            "env": {**env, "AUTOCAD_MCP_BACKEND": "ezdxf"},
        },
        "ifc": {
            "command": uvx,
            "args": ["ifc-mcp", "serve", "--transport", "stdio", "--quiet"],
            "env": env,
        },
    }
    if sys.platform == "win32" and REVIT_EXE.exists():
        servers["revit"] = {
            "command": str(REVIT_EXE),
            "args": ["--ManageConfigurationWithAutodeskRevitPluginInstaller=true"],
        }
        servers["mcp-server-for-revit"] = {
            "command": "cmd",
            "args": ["/c", "npx", "-y", "mcp-server-for-revit"],
        }
    return servers


def code_servers():
    uvx = tool("uvx")
    return {
        "autodesk-product-help": {"type": "http", "url": HELP_URL},
        "autodesk-fusion-data": {"type": "http", "url": FUSION_URL},
        "autocad": {
            "type": "stdio",
            "command": uvx,
            "args": ["--from", "autocad-mcp-pro", "autocad-mcp"],
            "env": {"AUTOCAD_MCP_BACKEND": "ezdxf", "PATH": path_env()},
        },
        "ifc": {
            "type": "stdio",
            "command": uvx,
            "args": ["ifc-mcp", "serve", "--transport", "stdio", "--quiet"],
            "env": {"PATH": path_env()},
        },
    }


def merge(path, servers):
    data = load_json(path)
    current = data.get("mcpServers") or {}
    current.update(servers)
    data["mcpServers"] = current
    save_json(path, data)
    return sorted(servers)


def main():
    desktop = desktop_config()
    added = merge(desktop, desktop_servers())
    print("Claude Desktop:", desktop)
    print("Ajoutés:", ", ".join(added))
    code = Path.home() / ".claude.json"
    if code.exists():
        code_added = merge(code, code_servers())
        print("Claude Code:", code)
        print("Ajoutés:", ", ".join(code_added))
    if sys.platform == "win32" and not REVIT_EXE.exists():
        print("Revit MCP officiel absent. Installez Revit 2027.2 puis le serveur Read-Tools depuis le compte Autodesk, et relancez ce script.")
    print("Fermez complètement Claude Desktop, puis rouvrez-le.")


if __name__ == "__main__":
    main()
