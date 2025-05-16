from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

NASA_API_KEY = "EMkRC4ae5uR7bkNVRToAfGhfrQHeBB7LVzCNtTEO"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        sol = request.form["sol"]
        return redirect(url_for("sol_weather", sol=sol))
    return render_template("index.html")

@app.route("/sol_weather")
def sol_weather():
    sol = request.args.get("sol")
    if sol and sol.isdigit():
        sol = int(sol)
        weather_url = "https://api.nasa.gov/insight_weather/"
        weather_params = {
            "api_key": NASA_API_KEY,
            "feedtype": "json",
            "ver": "1.0"
        }

        weather_response = requests.get(weather_url, params=weather_params)
        weather_data = weather_response.json()

        if str(sol) in weather_data:
            sol_data = weather_data[str(sol)]
            sol_int = sol

            image_url = None
            photo_api_url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
            photo_params = {
                "api_key": NASA_API_KEY,
                "sol": sol_int,
                "page": 1
            }

            photo_response = requests.get(photo_api_url, params=photo_params)
            photos = photo_response.json().get("photos", [])

            if photos:
                image_url = photos[0].get("img_src")
            else:
                image_url = "/static/placeholder.jpg"

            combined_data = {
                "sol": sol,
                "season": sol_data.get("Season", "N/A").capitalize(),
                "avg_temp": sol_data.get("AT", {}).get("av", "N/A"),
                "min_temp": sol_data.get("AT", {}).get("mn", "N/A"),
                "max_temp": sol_data.get("AT", {}).get("mx", "N/A"),
                "wind_speed": sol_data.get("HWS", {}).get("av", "N/A"),
                "pressure": sol_data.get("PRE", {}).get("av", "N/A"),
                "image": image_url
            }

            return render_template("sol_weather.html", weather=combined_data)
        else:
            return f"No data available for Sol {sol}."
    else:
        return "Invalid Sol number. Please enter a valid number."

if __name__ == "__main__":
    app.run(debug=True)