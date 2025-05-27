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


###using live cam design####
import streamlit as st
import cv2
import time
from mood_detection import detect_mood_face
from youtube_client import search_youtube_music
from feedback_manager import handle_feedback
from streamlit_lottie import st_lottie
import requests
import numpy as np  # Add this import for image processing
st.set_page_config(page_title="🎵 AI Mood-Based Music Generator", layout="wide")
# --- Load Lottie animation helper ---
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- Lottie animations for moods ---
lottie_animations = {
    "happy": load_lottie_url("https://assets4.lottiefiles.com/packages/lf20_touohxv0.json"),
    "sad": load_lottie_url("https://assets1.lottiefiles.com/packages/lf20_HpFqiS.json"),
    "neutral": load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_kkflmtur.json"),
    "angry": load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_jmgekfqg.json"),
    "surprise": load_lottie_url("https://assets8.lottiefiles.com/packages/lf20_e3i8qzql.json"),
    # Add more moods and links as needed
}

# --- Mood emojis ---
mood_emojis = {
    "happy": "😄",
    "sad": "😢",
    "neutral": "😐",
    "angry": "😠",
    "surprise": "😲",
}

# --- Mood background gradients ---
mood_colors = {
    "happy": "linear-gradient(135deg, #f6d365, #fda085)",
    "sad": "linear-gradient(135deg, #667eea, #764ba2)",
    "neutral": "linear-gradient(135deg, #89f7fe, #66a6ff)",
    "angry": "linear-gradient(135deg, #ff512f, #dd2476)",
    "surprise": "linear-gradient(135deg, #43cea2, #185a9d)",
}

# --- PAGE SETUP ---

# --- SESSION STATE INIT ---
for key, default_val in {
    "mood": None,
    "language": "English",
    "videos": [],
    "current_video": None,
    "run_webcam": False,
    "theme": "dark"
}.items():
    if key not in st.session_state:
        st.session_state[key] = default_val

# --- THEMES CSS ---
dark_theme_css = """
<style>
.stApp {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: #f0f2f6;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
h1 {
    font-size: 3.5rem;
    font-weight: 800;
    text-align: center;
    text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
    margin-bottom: 1rem;
}
h3 {
    color: #d1c4e9;
    font-weight: 600;
}
div.stButton > button:first-child {
    background-color: #6a11cb;
    color: white;
    font-size: 1.1rem;
    font-weight: 600;
    padding: 0.6rem 1.2rem;
    border-radius: 12px;
    border: none;
    box-shadow: 0 4px 15px rgba(106, 17, 203, 0.4);
    transition: background-color 0.3s ease, transform 0.2s ease;
}
div.stButton > button:first-child:hover {
    background-color: #8e2de2;
    cursor: pointer;
    transform: scale(1.05);
}
.container {
    background: rgba(255, 255, 255, 0.12);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.3);
}
.stImage img {
    border-radius: 14px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    transition: transform 0.3s ease;
}
.stImage img:hover {
    transform: scale(1.05);
}
iframe {
    border-radius: 16px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.4);
}
.stAlert {
    border-left: 6px solid #8e2de2 !important;
    background-color: rgba(142, 45, 226, 0.1) !important;
    color: #ede7f6 !important;
    padding: 1rem !important;
    border-radius: 12px !important;
}
.streamlit-spinner > div {
    font-weight: 700;
    font-size: 1.2rem;
    color: #d1c4e9 !important;
}
.feedback-container {
    margin-top: 1rem;
    display: flex;
    gap: 1rem;
}
</style>
"""

light_theme_css = """
<style>
.stApp {
    background: linear-gradient(135deg, #f6d365, #fda085);
    color: #3b2e2e;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
h1 {
    font-size: 3.5rem;
    font-weight: 800;
    text-align: center;
    text-shadow: 1px 1px 3px rgba(255,255,255,0.6);
    margin-bottom: 1rem;
}
h3 {
    color: #7f5a29;
    font-weight: 600;
}
div.stButton > button:first-child {
    background-color: #f6a560;
    color: #4b3621;
    font-size: 1.1rem;
    font-weight: 600;
    padding: 0.6rem 1.2rem;
    border-radius: 12px;
    border: none;
    box-shadow: 0 4px 15px rgba(246, 165, 96, 0.6);
    transition: background-color 0.3s ease, transform 0.2s ease;
}
div.stButton > button:first-child:hover {
    background-color: #f78f37;
    cursor: pointer;
    transform: scale(1.05);
}
.container {
    background: rgba(255, 255, 255, 0.85);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px 0 rgba(246, 165, 96, 0.25);
}
.stImage img {
    border-radius: 14px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.15);
    transition: transform 0.3s ease;
}
.stImage img:hover {
    transform: scale(1.05);
}
iframe {
    border-radius: 16px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.2);
}
.stAlert {
    border-left: 6px solid #f78f37 !important;
    background-color: rgba(247, 143, 55, 0.1) !important;
    color: #7f5a29 !important;
    padding: 1rem !important;
    border-radius: 12px !important;
}
.streamlit-spinner > div {
    font-weight: 700;
    font-size: 1.2rem;
    color: #f78f37 !important;
}
.feedback-container {
    margin-top: 1rem;
    display: flex;
    gap: 1rem;
}
</style>
"""

# Apply theme CSS
if st.session_state.theme == "dark":
    st.markdown(dark_theme_css, unsafe_allow_html=True)
else:
    st.markdown(light_theme_css, unsafe_allow_html=True)

# Apply mood-based background gradient if mood detected
if st.session_state.mood:
    bg_css = f"""
    <style>
    .stApp {{
        background: {mood_colors.get(st.session_state.mood, '#667eea')};
        transition: background 1s ease;
    }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.title("🎵 Mood Music Generator")
    st.markdown("""
    Welcome! This app detects your mood from your face using your webcam and
    plays YouTube music matching your mood and selected language.

    **How to Use:**
    1. Choose your preferred language.
    2. Click "Start Webcam Detection" and allow camera access.
    3. Wait ~2 seconds for mood detection.
    4. Enjoy music recommendations!  
    5. Like or Dislike songs to improve recommendations.
    6. Click "Next Song" to skip.

    *Built with Streamlit, OpenCV, and YouTube API.*
    """)
    st.markdown("---")

    # Language selector
    language = st.selectbox("Choose your language", ["English", "Hindi", "Tamil", "Telugu", "Kannada"])
    st.session_state.language = language

    # Theme toggle
    theme_option = st.radio("Theme", ["dark", "light"], index=0 if st.session_state.theme == "dark" else 1)
    st.session_state.theme = theme_option

# --- MAIN APP ---

st.title("🎶 AI Mood-Based Music Generator")

if not st.session_state.run_webcam:
    # Countdown before webcam start
    st.markdown("### Click the button below to start mood detection with your webcam")
    if st.button("📷 Start Webcam Detection"):
        st.session_state.run_webcam = True
        st.rerun()

else:
    st.markdown("### Get ready! Mood detection will start in...")

    countdown_placeholder = st.empty()
    for i in range(3, 0, -1):
        countdown_placeholder.markdown(
            f"<h1 style='text-align:center;color:#ff4b4b;'>{i}</h1>", unsafe_allow_html=True
        )
        time.sleep(1)
    countdown_placeholder.empty()

    st.markdown("### Detecting your mood...")

    cap = cv2.VideoCapture(0)
    webcam_placeholder = st.empty()

    if not cap.isOpened():
        st.error("⚠️ Cannot open webcam")
    else:
        ret = False
        frame = None

        # Show live feed for 3 seconds before capture
        start_time = time.time()
        while time.time() - start_time < 3:
            ret, frame = cap.read()
            if not ret:
                st.error("⚠️ Could not read frame from webcam")
                break
            # Convert frame to RGB for Streamlit
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            webcam_placeholder.image(frame_rgb, channels="RGB", caption="Live Webcam Feed")

        if ret:
            # Capture the last frame for mood detection
            with st.spinner("Detecting mood..."):
                mood = detect_mood_face(frame)
                st.session_state.mood = mood

            # Show the captured frame
            webcam_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB", caption="Captured Frame for Mood Detection")

        cap.release()

    # Reset run_webcam so user can retake if wanted
    st.session_state.run_webcam = False

# --- If mood detected, show results ---

# --- If mood detected, show results ---
if st.session_state.mood:
    mood = st.session_state.mood
    st.markdown(f"### Detected Mood: **{mood.capitalize()}** {mood_emojis.get(mood, '')}")

    # Show Lottie animation for mood if available
    if mood in lottie_animations and lottie_animations[mood]:
        st_lottie(lottie_animations[mood], height=200, key=f"lottie_{mood}")

    # Only fetch new videos if no videos are stored or mood has changed
    if not st.session_state.videos or st.session_state.videos[0].get("mood") != mood:
        videos = search_youtube_music(mood, st.session_state.language)

        # Optionally tag the mood in videos for validation
        for v in videos:
            v["mood"] = mood

        st.session_state.videos = videos

    if st.session_state.videos:
        video = st.session_state.videos[0]
        st.session_state.current_video = video
        video_link = video.get("link")

        if video_link:
            st.video(video_link)
            st.markdown(f"**Now Playing:** {video.get('title', 'Unknown')}  \n"
                        f"**Channel:** {video.get('channel', 'Unknown')}  \n"
                        f"**Duration:** {video.get('duration', 'Unknown')}")
        else:
            st.error("⚠️ Video link not found.")

        # Feedback buttons
        col1, col2, col3 = st.columns([1, 6, 1])
        with col1:
            if st.button("👍 Like"):
                handle_feedback(video.get("link"), liked=True)
        with col3:
            if st.button("👎 Dislike"):
                handle_feedback(video.get("link"), liked=False)
        with col2:
            if st.button("Next Song ▶️"):
                st.session_state.videos.append(st.session_state.videos.pop(0))
                st.rerun()

    else:
        st.warning("No videos found matching your mood and language.")

st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: black; font-size: 16px;'>"
    "Made with ❤️ by <strong><i>Jyothimayee<i></strong>. Enjoy the music! 🎧"
    "</div>",
    unsafe_allow_html=True
)
'''


###############################using picture for global use with design#################################################
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
st.set_page_config(page_title="🎵 AI Mood-Based Music Generator using YouTube", layout="wide")

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
        #st.image(frame, caption="Captured Image", use_container_width=True)

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
        st.info("📸 Please capture a photo after choosing a language to continue!")

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


