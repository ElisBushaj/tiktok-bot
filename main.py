import time
from math import ceil

import requests

# Constants
API_URL = "https://tiktok-views1.p.rapidapi.com"
HEADERS = {
    "X-RapidAPI-Key": "",
    "X-RapidAPI-Host": "tiktok-views1.p.rapidapi.com"
}


# The main function
def main():
    success_request_count = 0

    video_url: str = str(input("Enter the video url: "))
    views = int(input("Enter the number of views you want: "))

    total_iterations: int = ceil(views / 1000)
    if total_iterations < 1:
        print("The number of views should be greater than 1000")
        return

    print(f"Total iterations: {total_iterations}")

    while success_request_count < total_iterations:
        response = requests.get(f"{API_URL}/views?videoUrl={video_url}", headers=HEADERS)
        if response.status_code == 200:
            success_request_count += 1
            print(f"Request {success_request_count} was successful")
            print("Waiting for 125 seconds")
            time.sleep(125)

        else:
            print(f"Request {success_request_count} was not successful")
            response_data = response.json()
            if 'cooldownSeconds' in response_data:
                cooldown_seconds = response_data['cooldownSeconds']
                cooldown_seconds_int = int(cooldown_seconds)
                print(f"Waiting for {cooldown_seconds_int} seconds")
                time.sleep(cooldown_seconds_int + 5)
            elif response_data.get('message', '').startswith("You have exceeded the MONTHLY quota"):
                print(response_data['message'])
                break
            elif response_data.get('message', '').startswith("Invalid API key"):
                print(response_data['message'])
                break
            else:
                print(response_data)
                time.sleep(5)


if __name__ == '__main__':
    main()
