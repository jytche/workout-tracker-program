import requests
import datetime as dt
import os

api_id = os.environ["NUT_API_ID"]
api_key = os.environ["NUT_API_KEY"]

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

headers = {
    "x-app-id": f"{api_id}",
    "x-app-key": f"{api_key}",
    "x-remote-user-id": "0",
    "Content-Type": "application/json"
}

exercise = input("Tell me which exercises you did: ")

parameters = {
    "query": f"{exercise}",
    "gender": "male",
    "weight_kg": 72,
    "height_cm": 173,
    "age": 35
}

response = requests.post(url=exercise_endpoint, json=parameters, headers=headers)
exercise_data = response.json()
exercises = exercise_data['exercises']

now = dt.datetime.now()
today = now.date()
today_formatted = today.strftime("%d/%m/%Y")
time = now.time()
time_formatted = time.strftime("%H:%M:%S")

user = os.environ['SHEETY_USER']
password = os.environ['SHEETY_PASSWORD']
sheety_details = os.environ["SHEETY_ENDPOINT"]

exercise_list = [(exercise['name'], exercise['duration_min'], exercise['nf_calories']) for exercise in exercises]

for exercise in exercise_list:
    sheety_endpoint = f"{sheety_details}"

    sheety_params = {
        "workout": {
            "date": f"{today_formatted}",
            "time": f"{time_formatted}",
            "exercise": f"{exercise[0].title()}",
            "duration": f"{exercise[1]}",
            "calories": f"{exercise[2]}",
        }
    }

    sheety_response = requests.post(url=sheety_endpoint, json=sheety_params, auth=(user, password))
    response.raise_for_status()
    print(sheety_response.text)

