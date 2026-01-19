# ============================================================================
# SIMPLE SERVER - Creating a Web Server in Python
# ============================================================================

"""
A web server listens for requests and sends responses.
Python has a built-in module called http.server that makes this easy.
"""

# ============================================================================
# BASIC HTTP SERVER
# ============================================================================

"""
The http.server module lets you create a simple web server.
It serves files from the current directory.
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler

def start_server(port=8000):
    """
    Start a simple web server.
    
    Args:
        port: The port number (default: 8000)
    
    Usage:
        Call this function, then open http://localhost:8000 in your browser
    """
    # Create server address (empty string means 'localhost')
    server_address = ('', port)
    
    # Create the server
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    
    print(f"Server running at http://localhost:{port}/")
    print("Press Ctrl+C to stop")
    
    # Start the server (runs forever until stopped)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        httpd.shutdown()

# Run the server (uncomment the line below)
start_server(8000)


# ============================================================================
# HOW IT WORKS
# ============================================================================

"""
1. HTTPServer: Creates the server that listens for connections
2. SimpleHTTPRequestHandler: Handles requests and serves files
3. serve_forever(): Keeps the server running

When you visit http://localhost:8000 in your browser:
- Browser sends a request to the server
- Server responds with files from the current directory
- You see the files listed in your browser

To test:
1. Uncomment start_server(8000) above
2. Run the file: python index.py
3. Open http://localhost:8000 in your browser
4. Press Ctrl+C to stop the server
"""
