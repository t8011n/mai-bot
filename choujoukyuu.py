import json
import random


def abbr_dif(sheet):
    d = ""
    match sheet.get("difficulty", ""):
        case "basic": 
            d = "BAS"
        case "advanced":
            d = "ADV"
        case "expert":
            d = "EXP"
        case "master":
            d = "MAS"
        case "remaster":
            d = "Re:MAS"
        case _:  # 預設 fallback
            d = "不可能"
    return d


def MasterChoujoukyuu(json_path="data.json") -> list:
    # 讀取 JSON 檔案
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    cjk_sheets = []
    for song in data.get("songs", []):
        songName = song.get("songId", "")
        for sheet in song.get("sheets", []):
            #diff = abbr_dif(sheet)
            internalLevel = sheet.get("internalLevelValue", 0)
            if 14.5 <= internalLevel <= 14.9 and not sheet.get("type", "") == "utage":
                diff = abbr_dif(sheet)
                # songName = 
                level = str(internalLevel)
                entry = f"{songName} / {diff} ({internalLevel})"
                cjk_sheets.append(entry)

    fourSongs = []
    i = 0
    while i < 4:
        chosen = random.choice(cjk_sheets)
        fourSongs.append(chosen)
        i += 1
    
    return fourSongs