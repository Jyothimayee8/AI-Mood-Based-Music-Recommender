from youtubesearchpython import VideosSearch

def search_youtube_music(mood: str, language: str, max_results: int = 10) -> list:
    query = f"{mood} {language} music"
    try:
        videos_search = VideosSearch(query, limit=max_results)
        results = videos_search.result()
        videos = results.get('result', [])

        music_videos = []
        for video in videos:
            music_videos.append({
                "title": video.get('title', 'No Title'),
                "link": video.get('link'),
                "duration": video.get('duration', 'Unknown'),
                "channel": video.get('channel', {}).get('name', 'Unknown')
            })
        return music_videos
    except Exception as e:
        print(f"YouTube search failed: {e}")
        return []
