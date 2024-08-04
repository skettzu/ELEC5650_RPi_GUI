import requests
import random
import time

def test_google_apps_script():
    # URL of your deployed Google Apps Script web app
    url = "https://script.google.com/macros/s/AKfycbyZuUS5ln63BaxUhiVuu9_YmAhROL_30Y0pRwJfRwq43MD3-3x-syCX0weY3uGMd_tJ/exec"

    # Number of test iterations
    num_tests = 5

    for i in range(num_tests):
        # Generate random data for testing
        data = {
            "AccelX": round(random.uniform(-10, 10), 2),
            "AccelY": round(random.uniform(-10, 10), 2),
            "AccelZ": round(random.uniform(-10, 10), 2),
            "GyroX": round(random.uniform(-180, 180), 2),
            "GyroY": round(random.uniform(-180, 180), 2),
            "GyroZ": round(random.uniform(-180, 180), 2)
        }

        try:
            # Send GET request to the Google Apps Script web app
            response = requests.get(url, params=data)

            # Check the response
            if response.status_code == 200:
                print(f"Test {i+1} successful. Response: {response.text}")
            else:
                print(f"Test {i+1} failed. Status code: {response.status_code}")

            # Print the data sent
            print(f"Data sent: {data}")
            print("--------------------")

        except requests.RequestException as e:
            print(f"Error occurred during test {i+1}: {e}")

        # Wait for a short time between requests to avoid overwhelming the script
        time.sleep(2)

if __name__ == "__main__":
    test_google_apps_script()