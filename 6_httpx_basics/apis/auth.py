import httpx
from httpx_client import httpx_client

client = httpx_client()

def login():
    """Login to the API"""
    print("\n" + "="*60)
    print("1. LOGIN")
    print("="*60)
    
    # Create a client and make a request
    response = client.post('users/octocat', json={"username": "octocat", "password": "password"})
    
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Response Body: {response.json()}")
    
    # Check if request was successful
    if response.status_code == 200:
        data = response.json()
        print(f"\nUser: {data['name']}")
        print(f"Bio: {data['bio']}")


def sign_up():
    """Sign up to the API"""
    print("\n" + "="*60)
    print("2. SIGN UP")
    print("="*60)
    
    # Create a client and make a request
    response = client.post('users/octocat', json={"username": "octocat", "password": "password"})
    
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Response Body: {response.json()}")
    
    # Check if request was successful
    if response.status_code == 200:
        data = response.json()
        print(f"\nUser: {data['name']}")
        print(f"Bio: {data['bio']}")
