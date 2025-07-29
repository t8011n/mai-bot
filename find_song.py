import json

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


def find_difficulties(song):
    dif_st = []
    dif_dx = []
    for sheet in song.get("sheets", []): #sheetlist中 單一sheet迴圈
        sheet_type = sheet.get("type", "") 
        difficulty = abbr_dif(sheet)
        level = get_level(sheet)

        if sheet_type == "std":
            dif_st.append(f"{difficulty}: {level}")
        elif sheet_type == "dx":
            dif_dx.append(f"{difficulty}: {level}")

    dif_results = []
    if dif_st:
        dif_results.append("ST : " + " / ".join(dif_st))
    if dif_dx:
        dif_results.append("DX : " + " / ".join(dif_dx))
    
    return "\n".join(dif_results) if dif_results else "none" #st \n dx 

    '''
    all_difficulties = []
    for dif in song.get("sheets", []):
        dif_st = ""
        for one_dif in dif.get("type", ""):
            if one_dif["type"] == "std":
                dif_st += ("/" + one_dif["difficulty"] + "/" + one_dif["level"] + "/")
        dif_dx = ""
        for one_dif in sheets.get("type", ""):
            if one_dif["type"] == "dx":
                dif_dx += ("/" + one_dif["difficulty"] + "/" + one_dif["level"] + "/")

    '''


# 任何sheet中的 regions 的 intl is true
def IsIntl(song) -> bool:
    for sheet in song.get("sheets", []):
        if sheet.get("regions", {}).get("intl") == True:
            return True
    return False


# 有type不是utage 都不算宴譜
def IsUtage(song) -> bool:
    for sheet in song.get("sheets", []):
        if not sheet.get("type", "") == "utage":
            return False
    return True



def find_songs_by_keyword(keyword: str, json_path="data.json") -> list:
    # 讀取 JSON 檔案
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    results = []
    for song in data.get("songs", []):
        song_id = song.get("songId", "")
        #artist = song.get("artist", "")
        difficulties = find_difficulties(song)
        if keyword.lower() in song_id.lower() and IsIntl(song) and not IsUtage(song): 
            results.append(f"{song_id}\n{difficulties}")
        if len(results) >= 20:
            break
    
    if not results:
        return ["歌名為空，請重新輸入"]
    return results