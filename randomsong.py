import json
import random

def format_song(song):
    name = song.get("songId", "")
    artist = song.get("artist", "")
    version = song.get("version", "")
    return f"{name} - {artist} - {version}"

def random_song(json_path="data.json") -> list:
    # 讀取 JSON 檔案
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    songs = []
    for song in data.get("songs", {}):
        jp = False
        for sheet in song.get("sheets", []):
            if sheet.get("regions", {}).get("jp", "") == True:
                jp = True 
                break
        song_info = format_song(song)
        songs.append(song_info)

    chosen = random.choice(songs)
    return chosen
