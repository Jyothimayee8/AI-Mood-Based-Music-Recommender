import json
import os

FEEDBACK_FILE = "feedback_counter.json"

def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        try:
            with open(FEEDBACK_FILE, "r") as f:
                content = f.read().strip()
                return json.loads(content) if content else {}
        except json.JSONDecodeError:
            # If file is corrupted or empty, reset to empty dict
            return {}
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
