#!/usr/bin/env python3
"""Camofox Browser MCP Server — anti-detection browser backend for AI agents.

Wraps the camofox-browser REST API (localhost:9377) as MCP tools.
Requires: camofox-browser running (`npm start` in camofox-browser repo).

Usage:
    python scripts/camofox-mcp.py
    # or via mcp.json: "command": "python", "args": ["scripts/camofox-mcp.py"]

Env vars:
    CAMOFOX_URL  — base URL (default: http://localhost:9377)
"""

import os
import uuid

import httpx
from mcp.server.fastmcp import FastMCP

BASE_URL = os.environ.get("CAMOFOX_URL", "http://localhost:9377")
USER_ID = "claude-agent"
SESSION_KEY = f"mcp-{uuid.uuid4().hex[:8]}"
TIMEOUT = 30.0

mcp = FastMCP("camofox", instructions="Anti-detection browser. Use for sites that block bots.")

_client: httpx.Client | None = None


def client() -> httpx.Client:
    global _client
    if _client is None:
        _client = httpx.Client(base_url=BASE_URL, timeout=TIMEOUT)
    return _client


def _err(r: httpx.Response) -> str | None:
    """Return error string if response is not OK."""
    if r.status_code >= 400:
        try:
            data = r.json()
            return data.get("error", r.text)
        except Exception:
            return r.text
    return None


@mcp.tool()
def camofox_open(url: str) -> str:
    """Open a URL in a new anti-detection browser tab. Returns tab ID for subsequent actions."""
    r = client().post("/tabs", json={"userId": USER_ID, "sessionKey": SESSION_KEY, "url": url})
    if err := _err(r):
        return f"Error: {err}"
    data = r.json()
    return f"Tab opened: {data.get('tabId')} — {data.get('url')}"


@mcp.tool()
def camofox_snapshot(tab_id: str, include_screenshot: bool = False) -> str:
    """Get accessibility snapshot with element refs ([e1], [e2]...) for clicking/typing. Call after every navigation."""
    params = {"userId": USER_ID}
    if include_screenshot:
        params["includeScreenshot"] = "true"
    r = client().get(f"/tabs/{tab_id}/snapshot", params=params)
    if err := _err(r):
        return f"Error: {err}"
    data = r.json()
    result = data.get("snapshot", "")
    meta = []
    if data.get("truncated"):
        meta.append(f"truncated (offset={data.get('nextOffset', 0)})")
    if data.get("refsCount"):
        meta.append(f"{data['refsCount']} refs")
    if meta:
        result = f"[{', '.join(meta)}]\n{result}"
    if include_screenshot and data.get("screenshot"):
        result += f"\n\n[screenshot: {len(data['screenshot'].get('data', ''))} bytes base64]"
    return result


@mcp.tool()
def camofox_click(tab_id: str, ref: str) -> str:
    """Click an element by its ref (e.g. 'e1' from snapshot). After click, call snapshot again for fresh refs."""
    r = client().post(f"/tabs/{tab_id}/click", json={"userId": USER_ID, "ref": ref})
    if err := _err(r):
        return f"Error: {err}"
    data = r.json()
    msg = f"Clicked {ref}."
    if data.get("url"):
        msg += f" Now at: {data['url']}"
    if not data.get("refsAvailable", True):
        msg += " Refs invalidated — call snapshot to refresh."
    return msg


@mcp.tool()
def camofox_type(tab_id: str, ref: str, text: str) -> str:
    """Type text into an input field by ref (replaces existing content). Use camofox_press for Enter key."""
    r = client().post(f"/tabs/{tab_id}/type", json={"userId": USER_ID, "ref": ref, "text": text})
    if err := _err(r):
        return f"Error: {err}"
    return f"Typed into {ref}: '{text}'"


@mcp.tool()
def camofox_navigate(tab_id: str, url: str = "", macro: str = "", query: str = "") -> str:
    """Navigate to URL or use search macro (@google_search, @youtube_search, @amazon_search, @reddit_search, etc). Provide either url OR macro+query."""
    body: dict = {"userId": USER_ID}
    if macro:
        body["macro"] = macro
        body["query"] = query
    elif url:
        body["url"] = url
    else:
        return "Error: provide url or macro+query"
    r = client().post(f"/tabs/{tab_id}/navigate", json=body)
    if err := _err(r):
        return f"Error: {err}"
    data = r.json()
    msg = f"Navigated to {data.get('url', '?')}"
    if not data.get("refsAvailable", True):
        msg += " — call snapshot to get refs."
    if data.get("googleBlocked"):
        msg += " WARNING: Google blocked this request."
    return msg


@mcp.tool()
def camofox_screenshot(tab_id: str) -> str:
    """Take a screenshot of the current page. Returns base64 PNG data."""
    r = client().get(f"/tabs/{tab_id}/screenshot", params={"userId": USER_ID})
    if err := _err(r):
        return f"Error: {err}"
    data = r.json()
    b64 = data.get("data", "")
    return f"Screenshot captured ({len(b64)} bytes base64). MIME: {data.get('mimeType', 'image/png')}"


@mcp.tool()
def camofox_close(tab_id: str) -> str:
    """Close a browser tab. Always call when done to free resources."""
    r = client().delete(f"/tabs/{tab_id}", params={"userId": USER_ID})
    if err := _err(r):
        return f"Error: {err}"
    return f"Tab {tab_id} closed."


@mcp.tool()
def camofox_press(tab_id: str, key: str = "Enter") -> str:
    """Press a keyboard key (e.g. Enter, Tab, Escape). Use after camofox_type to submit forms."""
    r = client().post(f"/tabs/{tab_id}/press", json={"userId": USER_ID, "key": key})
    if err := _err(r):
        return f"Error: {err}"
    return f"Pressed {key}."


if __name__ == "__main__":
    mcp.run(transport="stdio")
