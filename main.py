from datetime import datetime
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from the correct .env file
load_dotenv("cred.env")

def get_exercise_stats(exercise_text):
    # Get Nutritionix credentials from environment variables
    app_id = os.getenv("NUTRITIONIX_APP_ID")
    api_key = os.getenv("NUTRITIONIX_API_KEY")

    url = 'https://trackapi.nutritionix.com/v2/natural/exercise'
    headers = {
        'Content-Type': 'application/json',
        'x-app-id': app_id,
        'x-app-key': api_key
    }
    data = {
        "query": exercise_text
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Request failed", "status_code": response.status_code}


def add_exercise_to_sheet(exercise_data):
    # Get Sheety URL and authorization from environment variables
    url = os.getenv("SHEETY_URL")
    authorization = os.getenv("SHEETY_AUTHORIZATION")

    # Get current date and time
    current_date = datetime.now().strftime('%d/%m/%Y')
    current_time = datetime.now().strftime('%H:%M:%S')

    for exercise in exercise_data["exercises"]:
        workout_data = {
            "workout": {
                "date": current_date,
                "time": current_time,
                "exercise": exercise['name'].capitalize(),
                "duration": exercise['duration_min'],
                "calories": exercise['nf_calories']
            }
        }

        headers = {
            "Authorization": authorization
        }

        response = requests.post(url, json=workout_data, headers=headers)

        if response.status_code == 200:
            print("Workout added to sheet:", response.json()['workout'])
        else:
            print("Failed to add workout:", response.status_code)

# Get exercise details from user and retrieve stats
exercise_text = input("Tell me which exercises you did: ")
stats = get_exercise_stats(exercise_text)

if "exercises" in stats:
    add_exercise_to_sheet(stats)
    print(json.dumps(stats, indent=2))
else:
    print("Error retrieving data:", stats.get("error", "Unknown error"))
