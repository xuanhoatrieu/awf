"""
Voice List v2 - Liet ke voices tu TTS server (OmniVoice Studio)
Chay: python voice_list.py
"""

import requests
import json
import sys
import os

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

API_URL = "http://117.0.36.6:8888"
API_KEY = "vneu_-q_okdL9TzB-sIMW1AQqNt0Z_qIoE05TN4s6H5snGEs"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}


def get_openapi_spec():
    """Get OpenAPI spec to discover all endpoints."""
    url = f"{API_URL}/openapi.json"
    resp = requests.get(url, timeout=10)
    if resp.status_code == 200:
        return resp.json()
    return None


def discover_voice_endpoints(spec):
    """Find all voice-related endpoints from OpenAPI spec."""
    paths = spec.get("paths", {})
    voice_endpoints = []
    tts_endpoints = []
    
    for path, methods in paths.items():
        path_lower = path.lower()
        if "voice" in path_lower or "speech" in path_lower or "tts" in path_lower or "audio" in path_lower:
            for method, details in methods.items():
                if method in ("get", "post", "put", "delete"):
                    voice_endpoints.append({
                        "method": method.upper(),
                        "path": path,
                        "summary": details.get("summary", ""),
                        "tags": details.get("tags", []),
                    })
    
    return voice_endpoints


def try_endpoint(method, path):
    """Try calling an endpoint and return response."""
    url = f"{API_URL}{path}"
    try:
        if method == "GET":
            resp = requests.get(url, headers=HEADERS, timeout=10)
        else:
            resp = requests.post(url, headers=HEADERS, timeout=10)
        
        if resp.status_code == 200:
            try:
                return resp.json()
            except json.JSONDecodeError:
                return resp.text[:500]
        return f"Status {resp.status_code}: {resp.text[:200]}"
    except Exception as e:
        return f"Error: {e}"


def main():
    print("=" * 60)
    print("  OmniVoice Studio - Voice Discovery")
    print("=" * 60)
    print(f"Server: {API_URL}")
    print()
    
    # Step 1: Get OpenAPI spec
    print("[1] Loading OpenAPI spec...")
    spec = get_openapi_spec()
    if not spec:
        print("  FAILED to load spec")
        return
    
    print(f"  API Title: {spec.get('info', {}).get('title', 'unknown')}")
    print(f"  Version: {spec.get('info', {}).get('version', 'unknown')}")
    print()
    
    # Step 2: Find voice endpoints
    print("[2] Discovering voice/audio endpoints...")
    endpoints = discover_voice_endpoints(spec)
    
    if not endpoints:
        print("  No voice endpoints found!")
        # Show all endpoints
        print("\n  All available endpoints:")
        for path, methods in spec.get("paths", {}).items():
            for m in methods:
                if m in ("get", "post"):
                    summary = methods[m].get("summary", "")
                    print(f"    {m.upper():6} {path:40} {summary}")
        return
    
    print(f"  Found {len(endpoints)} voice/audio endpoints:")
    for ep in endpoints:
        print(f"    {ep['method']:6} {ep['path']:40} {ep['summary']}")
    print()
    
    # Step 3: Call voice list endpoints
    print("[3] Fetching voice lists...")
    for ep in endpoints:
        if "list" in ep['summary'].lower() or "get" in ep['method'].lower():
            print(f"\n  >> {ep['method']} {ep['path']} ({ep['summary']})")
            result = try_endpoint(ep['method'], ep['path'])
            if isinstance(result, (dict, list)):
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(f"  {result}")
    
    # Step 4: Also show ALL paths for reference
    print("\n" + "=" * 60)
    print("[ALL ENDPOINTS]")
    for path, methods in sorted(spec.get("paths", {}).items()):
        for m in methods:
            if m in ("get", "post", "put", "delete"):
                summary = methods[m].get("summary", "")
                print(f"  {m.upper():6} {path:45} {summary}")


if __name__ == "__main__":
    main()
