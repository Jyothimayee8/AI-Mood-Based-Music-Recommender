import cv2
from deepface import DeepFace

def detect_mood_face(frame) -> str:
    try:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resized_frame = cv2.resize(rgb_frame, (640, 480))
        analysis = DeepFace.analyze(resized_frame, actions=["emotion"], enforce_detection=False)

        if isinstance(analysis, list):
            analysis = analysis[0]

        if "dominant_emotion" in analysis:
            return analysis["dominant_emotion"]
    except Exception as e:
        print("DeepFace error:", e)
    return None
