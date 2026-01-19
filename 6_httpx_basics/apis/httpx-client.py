import httpx

def httpx_client():
    return httpx.Client(
        base_url='https://api.github.com',
        headers={
            'User-Agent': 'MyGenAIApp/1.0',
            'Accept': 'application/json'
        },
        timeout=30.0
    )