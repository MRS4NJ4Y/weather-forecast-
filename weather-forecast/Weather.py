from flask import Flask, render_template, request  # Importing necessary Flask modules
import requests  # Importing the requests module to handle HTTP requests
from datetime import datetime  # Importing datetime to format timestamps
import webbrowser  # Importing webbrowser to open the app in a default web browser
from threading import Timer  # Importing Timer for delayed browser opening

# Creating a Flask app instance
app = Flask(__name__)

# Replace with your OpenWeatherMap API key
API_KEY = "757ef54a5805e041a88cf4c1eded4017"  # OpenWeatherMap API key for fetching weather data

@app.route("/", methods=["GET", "POST"])  # Defining a route for the home page, allowing GET and POST requests
def index():
    # Initialize variables for weather and forecast data and potential errors
    weather_data = None
    forecast_data = None
    error = None
    
    if request.method == "POST":  # Check if the request method is POST (user submitted the form)
        city = request.form.get("city")  # Get the city name from the form input
        if city:  # If a city name is provided
            # Construct the API URL for current weather and 5-day forecast
            current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
            
            # Fetch the current weather data
            current_response = requests.get(current_url)
            # Fetch the 5-day forecast data
            forecast_response = requests.get(forecast_url)

            # If both requests were successful
            if current_response.status_code == 200 and forecast_response.status_code == 200:
                # Parse the JSON responses into Python dictionaries
                weather_data = current_response.json()
                forecast_data = forecast_response.json()

                # Convert sunrise and sunset timestamps to readable time format (UTC)
                weather_data["sys"]["sunrise"] = datetime.utcfromtimestamp(
                    weather_data["sys"]["sunrise"]).strftime('%H:%M:%S')
                weather_data["sys"]["sunset"] = datetime.utcfromtimestamp(
                    weather_data["sys"]["sunset"]).strftime('%H:%M:%S')
            else:
                # If the city is not found or there's an error in the response
                error = "City not found. Please try again."
        else:
            # If the user submitted the form without entering a city
            error = "Please enter a city name."
    
    # Render the HTML template with weather data, forecast data, and error message
    return render_template("index.html", weather_data=weather_data, forecast_data=forecast_data, error=error)

# Function to open the default web browser with the app's URL
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

# Main entry point of the program
if __name__ == "__main__":
    Timer(1, open_browser).start()  # Start a timer to open the browser after 1 second
    app.run(debug=True)  # Run the Flask app in debug mode to allow real-time error tracking
