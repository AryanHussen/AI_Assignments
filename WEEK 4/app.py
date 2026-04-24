from flask import Flask, render_template, jsonify # Import Flask for the server, render_template for HTML, and jsonify for JSON responses
import json # Import the built-in json module to read the file

app = Flask(__name__) # Initialize the Flask web application instance

@app.route("/") # Define the route for the root URL (the homepage)
def index(): # Function that handles requests to the root URL
    return render_template("index.html") # Look in the 'templates' folder and serve the index.html file


@app.route("/data") # Define the route for the API endpoint that provides the history data
def data(): # Function that handles requests to the /data URL
    try: # Start a try block to handle potential file reading errors
        with open("history.json", "r") as f: # Open the history.json file in read mode
            return jsonify(json.load(f)) # Parse the JSON file into a Python list and return it as a JSON HTTP response
    except: # If an error occurs (like the file doesn't exist yet)
        return jsonify([]) # Return an empty JSON array to prevent the server from crashing


def run(): # Function to start the Flask server (called by main.py)
    app.run(port=5000, debug=False, use_reloader=False) # Start the server on port 5000, disable debug/reloader to avoid background thread issues
