import json

# 找不到internal level 就取 level
def get_level(sheet):
    #level = ""
    level = sheet.get("internalLevelValue")
    if level is None:
        level = sheet.get("level", "") #加入預設值 確保func return 不為空
    return str(level) 

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

def get_type(sheet):
    t = sheet.get("type", "")
    if t == "std":
        return "ST"
    elif t == "dx":
        return "DX"
    else:
        return "fghgyfkgjgjghkuvkythft"

def format_song(song_name, sheet, nd):
    #nd = 
    #song_name = song.get
    st_dx = get_type(sheet)
    difficulty = abbr_dif(sheet)
    level = get_level(sheet)
    return f"{nd} - {song_name} - {st_dx}/{difficulty}/{level}"

def find_nds(keyword: str, json_path="data.json") -> list:
    # 讀取 JSON 檔案
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    songs_info = []
    for song in data.get("songs", {}):
        song_name = song.get("songId", "")
        for sheet in song.get("sheets", []):
            #
            internalLevelValue = sheet.get("internalLevelValue", 0)
            if internalLevelValue <= 12: #目前不想看到level太低的，以後可能改成dict 讓level能排序
                continue
            #
            nd = sheet.get("noteDesigner")
            if nd is None:
                continue
            if keyword.lower() in nd.lower():  
                song_info = format_song(song_name, sheet, nd)
                songs_info.append(song_info)
        if len(songs_info) >= 20: #dc字元限制2000 還沒處理
            break

    if len(songs_info) == 0:
        return ["沒有"]     #先檢查再排序
    sorted_songs_info = sorted(songs_info)
    return sorted_songs_info


