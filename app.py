import streamlit as st
import cv2
import time
from mood_detection import detect_mood_face
from youtube_client import search_youtube_music
from feedback_manager import handle_feedback

st.set_page_config(page_title="AI Mood-Based Music Generator (YouTube)", layout="wide")
st.title("🎵 AI Mood-Based Music Generator using YouTube")

# Initialize session state
if "mood" not in st.session_state:
    st.session_state.mood = None
if "language" not in st.session_state:
    st.session_state.language = "English"
if "videos" not in st.session_state:
    st.session_state.videos = []
if "current_video" not in st.session_state:
    st.session_state.current_video = None
if "run_webcam" not in st.session_state:
    st.session_state.run_webcam = False

# Language selector
language = st.selectbox("Choose your preferred language:", ("English", "Hindi", "Telugu"))
st.session_state.language = language

def run_webcam_detection():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Could not open webcam")
        return None
    
    stframe = st.empty()
    detected_mood = None

    for _ in range(60):  # About 2 seconds (~30 fps * 2)
        ret, frame = cap.read()
        if not ret:
            st.warning("Failed to capture frame")
            break
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(rgb_frame, channels="RGB", caption="Webcam Live - Detecting Mood...")

        if detected_mood is None:
            detected_mood = detect_mood_face(frame)

        time.sleep(0.05)  # 20 FPS approx

    cap.release()
    stframe.empty()
    return detected_mood

if st.button("Detect Mood From Face"):
    st.session_state.run_webcam = True
    mood = run_webcam_detection()
    if mood:
        st.success(f"Detected Mood: {mood}")
        st.session_state.mood = mood
    else:
        st.warning("Could not detect mood from face.")
    st.session_state.run_webcam = False

if st.session_state.mood:
    st.subheader(f"🎧 Music for Mood: {st.session_state.mood}, Language: {st.session_state.language}")
    
    if not st.session_state.videos:
        st.session_state.videos = search_youtube_music(st.session_state.mood, st.session_state.language)

    if st.session_state.videos:
        video = st.session_state.videos[0]
        st.session_state.current_video = video

        st.markdown(f"### Now Playing: {video['title']}")
        st.markdown(f"Channel: {video['channel']}")
        st.markdown(f"Duration: {video['duration']}")

        # Extract video id from link
        video_id = video['link'].split("v=")[-1].split("&")[0]
        youtube_embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1"
        st.video(youtube_embed_url)

        # Like/Dislike buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👍 Like"):
                handle_feedback(video["link"], liked=True)
                st.success("You liked the song!")
        with col2:
            if st.button("👎 Dislike"):
                handle_feedback(video["link"], liked=False)
                st.error("You disliked the song.")

        if st.button("Next Song"):
            st.session_state.videos.pop(0)
            if st.session_state.videos:
                st.experimental_rerun()
            else:
                st.info("No more videos available for this mood/language.")
else:
    st.info("Click 'Detect Mood From Face' and select language to start playing music.")
