import time
import requests
from math import ceil
from typing import Dict, Any

# Constants
API_URL = "https://tiktok-views1.p.rapidapi.com"
HEADERS = {
    "X-RapidAPI-Key": "",
    "X-RapidAPI-Host": "tiktok-views1.p.rapidapi.com"
}

OPTIONS = [
    {"path": "views", "per_iteration": 1000},
    {"path": "shares", "per_iteration": 60},
    {"path": "saves", "per_iteration": 100}
]


def print_header():
    """Prints the bot header."""
    print("TIKTOK BOT")
    print("GitHub: @ElisBushaj")


def get_video_url() -> str:
    """Prompts the user for a video URL."""
    return input("Enter the video URL: ")


def select_option() -> int:
    """Prompts the user to select an action."""
    print("Options:")
    for index, option in enumerate(OPTIONS):
        print(f'{index + 1}. {option["path"].capitalize()}')

    while True:
        try:
            option = int(input("Select an option: ")) - 1
            if 0 <= option < len(OPTIONS):
                return option
            print("Invalid option. Please try again.")
        except ValueError:
            print("Please enter a valid number.")


def get_quantity(option: int) -> int:
    """Prompts the user for the desired quantity based on the selected option."""
    quantity = int(input(f"Enter the number of {OPTIONS[option]['path']} you want: "))
    return quantity


def calculate_iterations(quantity: int, per_iteration: int) -> int:
    """Calculates the total iterations needed."""
    return ceil(quantity / per_iteration)


def handle_api_response(response: requests.Response, success_count: int, cooldown: int) -> int:
    """Handles the API response and applies any necessary cooldowns."""
    if response.status_code == 200:
        print(f"Request {success_count + 1} was successful.")
        return cooldown
    else:
        response_data = response.json()
        message = response_data.get('message', '')

        if 'cooldownSeconds' in response_data:
            cooldown_seconds = int(response_data['cooldownSeconds'])
            print(f"Waiting for {cooldown_seconds + 5} seconds due to API cooldown.")
            return cooldown_seconds + 5
        elif "exceeded the MONTHLY quota" in message or "Invalid API key" in message:
            print(message)
            return -1  # Stop processing
        else:
            print(f"Error: {response_data}")
            return 5  # General wait time for other errors


def make_requests(video_url: str, total_iterations: int, selected_option: Dict[str, Any]) -> None:
    """Makes API requests based on user input and handles the responses."""
    success_request_count = 0

    while success_request_count < total_iterations:
        response = requests.get(f"{API_URL}/{selected_option['path']}", params={"videoUrl": video_url}, headers=HEADERS)
        cooldown = handle_api_response(response, success_request_count, 0)

        if cooldown == -1:
            break

        success_request_count += 1
        if success_request_count < total_iterations:
            time.sleep(125)  # Wait between requests

        if cooldown > 0:
            time.sleep(cooldown)


def main():
    print_header()

    video_url = get_video_url()
    selected_option_index = select_option()
    selected_option = OPTIONS[selected_option_index]

    quantity = get_quantity(selected_option_index)
    total_iterations = calculate_iterations(quantity, selected_option['per_iteration'])

    if total_iterations < 1:
        print(f"The number of {selected_option['path']} should be greater than {selected_option['per_iteration']}.")
        return

    print(f"Total iterations: {total_iterations}")
    make_requests(video_url, total_iterations, selected_option)


if __name__ == '__main__':
    main()
