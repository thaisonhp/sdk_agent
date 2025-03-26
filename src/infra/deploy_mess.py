import requests

ACCESS_TOKEN = "EAAQy1i2hfz4BO1sVZCxPndDqffHKCZBhxAPf3qIQkYMzmO1lLlZBoj9VToiRtyCKBfaOkUZAVKkqxDprcS8iXBuvg9HZBScAYmQVqVuc25qagt6HOdrMZAb1nbLZACjT0WL0KYj0BiHnkdDZCehRoEHK9Qc6ZAZCz1iUhR86oEPZCJCLmqCNUumru8UuB30IoSTLntZCXknScsElvrogCsCp9Y0W13mMxnFvPoPpnDBpYQBFb4ONqZCBGsvf7"
USER_ID = "654837487092155"

url = "https://graph.facebook.com/v17.0/me/messages"

payload = {
    "recipient": {"id": USER_ID},
    "message": {"text": "Xin chào! Tôi là chatbot Messenger."}
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
