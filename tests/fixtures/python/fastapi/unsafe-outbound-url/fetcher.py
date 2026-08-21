def mock_fetch(url: str):
    # VULNERABLE: Direct URL fetch without SSRF controls
    return {"url": url, "status": "fetched"}
