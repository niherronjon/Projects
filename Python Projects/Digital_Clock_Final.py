import tkinter as tk
import requests
from datetime import datetime
from geopy.geocoders import Nominatim
import math

# Constants
API_KEY = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your OpenWeatherMap API key

# Initialize main window
root = tk.Tk()
root.title("Digital and Analog Clock with Weather")
root.geometry("500x500")
root.configure(bg="white")

# Circle canvas
canvas = tk.Canvas(root, width=400, height=400, bg="white", highlightthickness=0)
canvas.pack(pady=20)

# Labels for Time, Date, Day, Temperature, and Location with specified colors and formatting
time_label = tk.Label(root, font=("Helvetica", 20, "bold"), fg="green", bg="white")
date_label = tk.Label(root, font=("Helvetica", 20), fg="blue", bg="white")
day_label = tk.Label(root, font=("Helvetica", 15, "bold"), fg="black", bg="white")
temperature_label = tk.Label(root, font=("Helvetica", 15), bg="white", fg="blue")
location_label = tk.Label(root, font=("Helvetica", 15), bg="white", fg="green")

time_label.pack()
date_label.pack()
day_label.pack()
temperature_label.pack(pady=5)
location_label.pack()

# Function to update the digital clock with 12-hour format
def update_time():
    now = datetime.now()
    current_time = now.strftime("%I:%M:%S %p")  # 12-hour format with AM/PM
    current_date = now.strftime("%Y-%m-%d")
    current_day = now.strftime("%A")
    
    time_label.config(text=f"Time: {current_time}")
    date_label.config(text=f"Date: {current_date}")
    day_label.config(text=f"Day: {current_day}")
    
    # Schedule the function to run again after 1 second
    root.after(1000, update_time)

# Function to fetch device location temperature from OpenWeatherMap API
def fetch_temperature():
    try:
        # Use geopy to get the user's approximate location by IP
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode("New York")  # Replace with "auto-ip" based on real location
        city = location.address
        latitude, longitude = location.latitude, location.longitude

        # API request to OpenWeatherMap
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={API_KEY}"
        response = requests.get(url)
        data = response.json()
        
        # Extract temperature and city information
        if data["cod"] == 200:
            temp = data["main"]["temp"]
            temperature_label.config(text=f"Temperature: {temp}°C")
            location_label.config(text=f"Location: {city}")
        else:
            temperature_label.config(text="Temperature: N/A")
            location_label.config(text="Location: N/A")
    except Exception as e:
        temperature_label.config(text="Temperature: N/A")
        location_label.config(text="Location: N/A")
        print("Error fetching temperature:", e)

# Function to draw analog clock in the canvas
def draw_analog_clock():
    now = datetime.now()
    sec = now.second
    minute = now.minute
    hour = now.hour % 12 + minute / 60

    # Calculate angles
    sec_angle = math.radians(6 * sec - 90)
    min_angle = math.radians(6 * minute - 90)
    hour_angle = math.radians(30 * hour - 90)

    # Coordinates for clock hands
    sec_x, sec_y = 200 + 80 * math.cos(sec_angle), 200 + 80 * math.sin(sec_angle)
    min_x, min_y = 200 + 70 * math.cos(min_angle), 200 + 70 * math.sin(min_angle)
    hour_x, hour_y = 200 + 50 * math.cos(hour_angle), 200 + 50 * math.sin(hour_angle)

    # Clear canvas and redraw clock face
    canvas.delete("hands")
    canvas.create_oval(100, 100, 300, 300, outline="black", width=4)

    # Draw hour, minute, and second hands
    canvas.create_line(200, 200, hour_x, hour_y, fill="black", width=6, tags="hands")
    canvas.create_line(200, 200, min_x, min_y, fill="blue", width=4, tags="hands")
    canvas.create_line(200, 200, sec_x, sec_y, fill="red", width=2, tags="hands")

    # Schedule the function to run again after 1000 ms
    root.after(1000, draw_analog_clock)

# Initial calls to update time, fetch temperature, and draw the analog clock
update_time()
fetch_temperature()
draw_analog_clock()

# Run the Tkinter event loop
root.mainloop()