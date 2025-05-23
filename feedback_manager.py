import json
import os

FEEDBACK_FILE = "feedback_data.json"

def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r") as f:
            return json.load(f)
    return {}

def save_feedback(data):
    with open(FEEDBACK_FILE, "w") as f:
        json.dump(data, f, indent=4)

def handle_feedback(video_link, liked: bool):
    data = load_feedback()
    if video_link not in data:
        data[video_link] = {"likes": 0, "dislikes": 0}
    if liked:
        data[video_link]["likes"] += 1
    else:
        data[video_link]["dislikes"] += 1
    save_feedback(data)
