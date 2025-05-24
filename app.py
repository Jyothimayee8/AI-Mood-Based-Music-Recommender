###################################USING LIVE CAM WORKS IN NORMAL ENVIRONMENT(LOCAL USE)########################################
'''
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
language = st.selectbox("Choose your preferred language:", ("English", "Hindi", "Telugu","Tamil","Kannada"))
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


#####USING PICTUREEEE (FOR GLOBAL USE DURING DEPLOYMENT)###########################
import streamlit as st
import time
from mood_detection import detect_mood_face
from youtube_client import search_youtube_music
from feedback_manager import handle_feedback
from PIL import Image
import numpy as np

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

# Language selector
language = st.selectbox("Choose your preferred language:", ("English", "Hindi", "Telugu","Tamil","Kannada"))
st.session_state.language = language

# Camera input
image_data = st.camera_input("Take a picture to detect your mood")

if image_data is not None:
    img = Image.open(image_data)
    frame = np.array(img)

    st.image(frame, caption="Captured Image", use_container_width=True)

    with st.spinner("Analyzing mood..."):
        mood = detect_mood_face(frame)

    if mood:
        st.success(f"Detected Mood: {mood}")
        st.session_state.mood = mood
    else:
        st.warning("Could not detect mood from face.")

# Display music if mood is detected
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

        video_id = video['link'].split("v=")[-1].split("&")[0]
        youtube_embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1"
        st.video(youtube_embed_url)

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
                st.rerun()
            else:
                st.info("No more videos available for this mood/language.")
else:
    st.info("Take a photo and select language to start playing music.")


'''

import streamlit as st
import time
from mood_detection import detect_mood_face
from youtube_client import search_youtube_music
from feedback_manager import handle_feedback
from streamlit_lottie import st_lottie
from PIL import Image
import numpy as np
import requests

# --- Page Setup ---
st.set_page_config(page_title="🎵 AI Mood-Based Music Generator (YouTube)", layout="wide")

# --- Load Lottie animations ---
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_animations = {
    "happy": load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_touohxv0.json"),
    "sad": load_lottie_url("https://assets1.lottiefiles.com/packages/lf20_HpFqiS.json"),
    "neutral": load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_kkflmtur.json"),
    "angry": load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_jmgekfqg.json"),
    "surprise": load_lottie_url("https://assets8.lottiefiles.com/packages/lf20_e3i8qzql.json"),
    "music_bar": load_lottie_url("https://assets8.lottiefiles.com/packages/lf20_cycgflhv.json")
}

mood_emojis = {
    "happy": "😄",
    "sad": "😢",
    "neutral": "😐",
    "angry": "😠",
    "surprise": "😲",
}

# --- CSS Styling ---
st.markdown("""
<style>
    .bright-info {
    color: #7de1b8 !important;
    font-weight: 700;
    font-size: 22px;
    text-align: center;
    text-shadow: 0 0 8px #7de1b8, 0 0 12px #5bd1a4;
    margin-top: 40px;
    margin-bottom: 20px;
}

.stApp {
    background: #0f1a2b;  /* deep navy */
    color: #dce7ff;       /* soft light blue text */
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    min-height: 100vh;
    padding: 20px 40px;
}

h1, h2, h3 {
    text-align: center;
    font-weight: 700;
    letter-spacing: 1.4px;
    margin-bottom: 10px;
    color: #dce7ff;
}

.stImage img {
    border-radius: 15px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
    margin-top: 15px;
}

.stButton > button {
    border-radius: 25px;
    padding: 14px 32px;
    font-size: 18px;
    font-weight: 700;
    background: #5bd1a4;  /* pastel teal */
    color: #0f1a2b;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease-in-out;
    box-shadow: 0 5px 15px rgba(91, 209, 164, 0.6);
    margin-top: 10px;
    width: 100%;
}

.stButton > button:hover {
    background: #7de1b8; /* brighter teal */
    box-shadow: 0 7px 22px rgba(125, 225, 184, 0.9);
    transform: scale(1.1);
    color: #0b130f;
}

.stSelectbox > div[data-baseweb="select"] {
    background-color: #15253f;  /* lighter navy */
    color: #5bd1a4;  /* pastel teal text */
    border-radius: 14px;
    font-weight: 600;
    font-size: 16px;
    padding: 8px;
    box-shadow: 0 4px 12px rgba(91, 209, 164, 0.5);
    margin-bottom: 20px;
}

.stSelectbox > div[data-baseweb="select"]:hover {
    background-color: #1e3258;
    color: #7de1b8;
}

.stAlert {
    border-radius: 12px !important;
    padding: 15px !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    color: #dce7ff !important;
}

.css-1d391kg .element-container {
    padding-left: 30px !important;
    padding-right: 30px !important;
}

footer {
    text-align: center;
    margin-top: 30px;
    font-size: 14px;
    color: #7de1b8;
}
</style>
""", unsafe_allow_html=True)

# --- Title Row ---
st.title("🎶 AI Mood-Based Music Generator Using YouTube")

if lottie_animations["music_bar"]:
    st_lottie(lottie_animations["music_bar"], height=120, key="musicbar")

# --- Session State Init ---
for key, val in {
    "mood": None,
    "language": "English",
    "videos": [],
    "current_video": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# --- Layout Split ---
col1, col2 = st.columns([1, 2])

with col1:
    st.header("🌐 Language & Mood")
    language = st.selectbox("Choose Language:", ("English", "Hindi", "Telugu", "Tamil", "Kannada"))
    st.session_state.language = language

    st.subheader("📸 Capture your Mood")
    image_data = st.camera_input("Take a picture")

    if image_data:
        img = Image.open(image_data)
        frame = np.array(img)
        st.image(frame, caption="Captured Image", use_container_width=True)

        with st.spinner("Analyzing mood..."):
            mood = detect_mood_face(frame)

        if mood:
            st.session_state.mood = mood
            st.success(f"Mood Detected: {mood_emojis.get(mood, '')} {mood.capitalize()}")
            if lottie_animations.get(mood):
                st_lottie(lottie_animations[mood], height=250, key="mood_animation")
        else:
            st.warning("Could not detect mood from the captured face.")

with col2:
    if st.session_state.mood:
        st.subheader(f"🎧 Songs for: {mood_emojis.get(st.session_state.mood)} {st.session_state.mood.capitalize()} in {st.session_state.language}")

        if not st.session_state.videos:
            st.session_state.videos = search_youtube_music(st.session_state.mood, st.session_state.language)

        if st.session_state.videos:
            video = st.session_state.videos[0]
            st.session_state.current_video = video

            st.markdown(f"### ▶️ Now Playing: **{video['title']}**")
            st.markdown(f"**Channel:** {video['channel']} | **Duration:** {video['duration']}")

            video_id = video['link'].split("v=")[-1].split("&")[0]
            youtube_embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1"
            st.video(youtube_embed_url)

            col_like, col_dislike = st.columns(2)
            with col_like:
                if st.button("👍 Like"):
                    handle_feedback(video["link"], liked=True)
                    st.success("You liked the song!")
            with col_dislike:
                if st.button("👎 Dislike"):
                    handle_feedback(video["link"], liked=False)
                    st.error("You disliked the song.")

            if st.button("⏭️ Next Song"):
                st.session_state.videos.pop(0)
                if st.session_state.videos:
                    st.rerun()
                else:
                    st.info("No more videos for this mood/language.")
    else:
        st.info("📸 Please capture a photo and choose a language to continue!")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #e0d9ff; font-size: 16px; font-weight: 600;'>
    Made with ❤️ by <strong><i>Jyothimayee</i></strong>. Enjoy the music! 🎧
</div>
""", unsafe_allow_html=True)
# --- SIDEBAR ---
with st.sidebar:
    st.title("🎵 Mood Music Generator")
    st.markdown("""
    Welcome! This app detects your mood from your face using your webcam and
    plays YouTube music matching your mood and selected language.

    **How to Use:**
    1. Choose your preferred language.
    2. Capture a photo using your webcam.
    3. Let the app analyze your mood.
    4. Enjoy music recommendations based on your mood.  
    5. Like or Dislike songs to improve future suggestions.
    6. Use "Next Song" to skip to the next recommended track.
    """)
