import json
import requests
from datetime import datetime

with open("config.json") as json_data_file:
    config_data = json.load(json_data_file)

APP_ID = config_data["nutritionix"]["applicationID"]
API_KEY = config_data["nutritionix"]["apikey"]
AUTH = config_data["sheety"]["auth"]

nutritionix_url = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_url = "https://api.sheety.co/4b76a52212be69c9c166005b9184b9d9/workoutTracking/workouts"

nutritionix_headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY
}

sheety_headers = {
    "Authorization": f"Basic {AUTH}"
}

query = input("Tell me which exercise you did: ")

params = {
    "query": query,
    "gender": "male",
    "weight_kg": 70,
    "height_cm": 178,
    "age": 37
}

response = requests.post(url=nutritionix_url, json=params, headers=nutritionix_headers)
response.raise_for_status()
data = response.json()
print(data)

now = datetime.now()
exercise_date = datetime.strftime(now, '%d/%m/%Y')
exercise_time = datetime.strftime(now, '%H:%M:%S')

for exercise in data['exercises']:
    sheety_inputs = {
        "workout": {
            "date": exercise_date,
            "time": exercise_time,
            "exercise": exercise['name'].title(),
            "duration": exercise['duration_min'],
            "calories": exercise['nf_calories']
        }
    }

    sheety_response = requests.post(url=sheety_url, json=sheety_inputs, headers=sheety_headers)
    print(sheety_response.text)

