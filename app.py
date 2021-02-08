import requests
from configparser import ConfigParser
from flask import Flask, render_template, request, redirect, url_for

# Application only works for USA zip codes!

app = Flask(__name__)

# Returns home html where zip_code should be provided for completing the action!
@app.route("/")
def weather_dashbord():
    return render_template("home.html")

# Main function returns values for the zip code you provided! 
@app.route("/results", methods = ["POST"])
def render_results():
    # Accessing my zip code!
    zip_code = request.form.get("zipCode")
    # Accessing my api!
    api_key = get_api_key()
    # Geting the data with function I create later
    data = get_weather_results(zip_code, api_key)

    # Accessing specific data!
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    weather = data["weather"][0]["main"]
    location = data["name"]
    
    # Adding data to index.html so that you can see it!
    return render_template("index.html", location = location, temp = temp, feels_like = feels_like, weather = weather)

@app.route("/return_back", methods = ["GET"])
def return_back():
    return redirect(url_for("weather_dashbord"))


# Function that returns my api
def get_api_key():
    config = ConfigParser()
    config.read("config.ini")
    return config['openweathermap']['api']

# Function that is used for getting all the data for the zip code you provided!
def get_weather_results(zip_code, api_key):
    api_url = f"http://api.openweathermap.org/data/2.5/weather?zip={zip_code}&units=metric&appid={api_key}"
    r = requests.get(api_url)
    return r.json()




if __name__ == "__main__":
    app.run(debug=True)

