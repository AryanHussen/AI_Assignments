import json # Import the built-in json module to read the file and format responses
from http.server import BaseHTTPRequestHandler, HTTPServer # Import built-in server classes

class RequestHandler(BaseHTTPRequestHandler): # Create a custom class to handle HTTP requests
    
    def do_GET(self): # Function that handles all incoming GET requests
        
        # Define the route for the root URL (the homepage)
        if self.path == "/":
            self.send_response(200) # Send a 200 OK status code
            self.send_header("Content-type", "text/html") # Tell the browser we are sending HTML
            self.end_headers() # Finish sending headers
            
            try:
                # Flask automatically looks in a 'templates' folder, so we replicate that here
                with open("templates/index.html", "rb") as f:
                    self.wfile.write(f.read()) # Send the contents of index.html to the browser
            except FileNotFoundError:
                self.wfile.write(b"Error: templates/index.html not found.")
                
        # Define the route for the API endpoint that provides the history data
        elif self.path == "/data":
            self.send_response(200) # Send a 200 OK status code
            self.send_header("Content-type", "application/json") # Tell the browser we are sending JSON
            self.end_headers() # Finish sending headers
            
            try: # Start a try block to handle potential file reading errors
                with open("history.json", "r") as f: # Open the history.json file in read mode
                    data = json.load(f) # Parse the JSON file into a Python list
                    # Convert back to a JSON string, encode to bytes, and send it
                    self.wfile.write(json.dumps(data).encode("utf-8")) 
            except: # If an error occurs (like the file doesn't exist yet)
                # Return an empty JSON array to prevent the server from crashing
                self.wfile.write(json.dumps([]).encode("utf-8"))
                
        # Handle 404 Not Found for any other routes
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"404 Not Found")


def run(): # Function to start the vanilla Python server
    port = 5000
    server_address = ('', port) # Bind to all available interfaces on port 5000
    httpd = HTTPServer(server_address, RequestHandler) # Initialize the server instance
    print(f"Server running on port {port}...")
    httpd.serve_forever() # Start the server and keep it running

# If this file is run directly, start the server
if __name__ == "__main__":
    run()
