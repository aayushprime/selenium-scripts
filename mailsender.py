import requests


def sendemail(data):
    cookies = {}
    headers = {}
    receiver_email = "lamichhaneaayush9@gmail.com"
    data = {
        "name": "Seed Found!",
        "message": data,
        "email": receiver_email,
    }

    response = requests.post(
        "https://script.google.com/macros/s/AKfycbwWdhMeY54pzEVCvC6MJpwXvWqzBfLFck9cFGZgX8aBo_1L-LRYFxN13gJXQZVYPzSc/exec",
        cookies=cookies,
        headers=headers,
        data=data,
    )
    if response.json()["result"] == "success":
        print("Email sent successfully")
    else:
        raise Exception("Email not sent")


if __name__ == "__main__":
    sendemail("Test Data")
