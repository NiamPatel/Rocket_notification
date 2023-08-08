import time
from flask import Flask, render_template
from twilio.rest import Client
import requests

app = Flask(__name__)

# Replace these with your Twilio credentials
TWILIO_ACCOUNT_SID = 'AC415ee83c07ceb79f16999c3b66af9c07'
TWILIO_AUTH_TOKEN = '927d9d468f36547db21594a8d68805ba'
TWILIO_PHONE_NUMBER = '+18559109211'

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


# Function to check for upcoming launches
def check_launches():
    while True:
        try:
            # Fetch upcoming launches from Launch Library API
            response = requests.get("https://launchlibrary.net/1.3/launch/upcoming")
            data = response.json()

            # Extract launch details from the response
            if "launches" in data:
                for launch in data["launches"]:
                    launch_name = launch["name"]
                    launch_time = launch["net"]
                    launch_location = launch["location"]["name"]
                    look_direction = "Unknown"  # Replace with actual calculation

                    # Send notifications for upcoming launches
                    message = (
                        f"Rocket launch alert!\n"
                        f"Launch Name: {launch_name}\n"
                        f"Launch Time: {launch_time}\n"
                        f"Launch Location: {launch_location}\n"
                        f"Look Direction: {look_direction}"
                    )

                    # Replace with actual phone numbers
                    phone_numbers = ["+12068808303",]
                    for phone_number in phone_numbers:
                        twilio_client.messages.create(
                            body=message,
                            from_=TWILIO_PHONE_NUMBER,
                            to=phone_number
                        )

            time.sleep(3600)  # Check every hour

        except Exception as e:
            print("An error occurred:", e)
            time.sleep(3600)  # Retry after an hour


@app.route('/')
def index():
    return "Rocket launch notifier is running!"


if __name__ == '__main__':
    # Start the launch checking process in a separate thread
    import threading

    launch_thread = threading.Thread(target=check_launches)
    launch_thread.start()

    app.run(debug=True)
