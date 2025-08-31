import requests

def get_pairs():
    """
    Henter token-par fra DEX Screener API og returnerer en liste af dicts.
    Felter: pairAddress, baseSymbol, quoteSymbol, priceUsd, liquidityUsd, dexId, chainId.
    """
    url = "https://api.dexscreener.com/latest/dex/pairs"
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"Fejl ved hentning af data: {e}")
        return []

    results = []
    for pair in data.get("pairs", []):
        results.append({
            "pairAddress": pair.get("pairAddress"),
            "baseSymbol": (pair.get("baseToken") or {}).get("symbol"),
            "quoteSymbol": (pair.get("quoteToken") or {}).get("symbol"),
            "priceUsd": pair.get("priceUsd"),
            "liquidityUsd": (pair.get("liquidity") or {}).get("usd"),
            "dexId": pair.get("dexId"),
            "chainId": pair.get("chainId"),
        })
    return results
