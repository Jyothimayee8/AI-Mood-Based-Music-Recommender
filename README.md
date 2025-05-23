# AI Mood-Based Music Recommender (YouTube)

A real-time AI-powered web app that detects your mood through facial expressions and plays mood-aligned music from YouTube in your preferred language.

---

## Features

- **Real-time mood detection:** Uses webcam input with OpenCV and DeepFace to analyze facial expressions and detect your mood instantly.
- **YouTube music search and playback:** Automatically searches YouTube for music matching the detected mood and selected language (English, Hindi, Telugu) and plays it within the app.
- **Interactive UI:** Built with Streamlit, includes live webcam feed, embedded YouTube video player, and controls like like/dislike and next song.
- **Feedback system:** Allows users to like or dislike songs to personalize and improve future recommendations.

---

## Tech Stack

- **Python** – Core programming language.
- **Streamlit** – Web application framework for rapid UI development.
- **OpenCV** – Real-time computer vision for webcam capture.
- **DeepFace** – State-of-the-art facial emotion recognition.
- **YouTube Search Python API** – For querying and retrieving YouTube music videos.

---

## Installation

### Prerequisites

- Python 3.7 or above installed on your system.
- Webcam connected for mood detection.

### Steps

1. Clone the repository:

```bash
git clone https://github.com/jyothimayee8/ai-mood-music.git
cd ai-mood-music
````

2. Install required Python packages:

```bash
pip install -r requirements.txt
```

---

## Usage

**1. Run the Streamlit app:**

```bash
streamlit run app.py
```

2. The app will open in your default browser.

3. Click **Detect Mood From Face** to activate your webcam and detect your mood.

4. Select your preferred language from the dropdown menu.

5. The app will display and autoplay YouTube music videos that match your mood and language.

6. Use the **Like** or **Dislike** buttons to provide feedback on songs.

7. Click **Next Song** to skip to the next music video.

---

## Dependencies

This project relies on the following Python libraries:

* `streamlit`
* `opencv-python`
* `deepface`
* `youtube-search-python`
* `pafy`
* `youtube_dl`

All dependencies are listed in the `requirements.txt` file for easy installation.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

* [DeepFace](https://github.com/serengil/deepface) – for facial emotion recognition.
* [YouTube Search Python](https://github.com/alexmercerind/youtube-search-python) – for fetching YouTube music videos.
* [Streamlit](https://streamlit.io/) – for the web app framework.
* [OpenCV](https://opencv.org/) – for webcam video capture.

---

## Contact

You can find me on GitHub: [jyothimayee8](https://github.com/jyothimayee8).
Feel free to reach out for collaboration or questions!

---

## About this Project

This project integrates AI-driven emotion detection with dynamic multimedia streaming to enhance user experience by playing music that fits their mood. It demonstrates skills in computer vision, API integration, real-time video processing, and user interaction design.

---

Thank you for checking out my project! 🎶😊

```
