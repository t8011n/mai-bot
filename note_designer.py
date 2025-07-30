import json

def find_nd(keyword: str, json_path="data.json") -> list:
    # 讀取 JSON 檔案
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    note_designers = []
    for song in data.get("songs", {}):
        for sheet in song.get("sheets", []):
            # nd = sheet.get("noteDesigner", "") ← X *註 最下面
            nd = sheet.get("noteDesigner")
            if nd is None:
                continue
            if keyword.lower() in nd.lower() and nd not in note_designers:  # ← ✅ 補：避免重複加入
                note_designers.append(nd)  # ← ✅ 補：直接 append nd 就好，不必 .append(f"{nd}")
        if len(note_designers) >= 50: #dc 字元限制2000 還沒處理
            break

    sorted_note_designers = sorted(note_designers)

    if len(note_designers) == 0:
        return ["不知道"] # ← ✅ 建議：回傳 list，與函式標註一致
    return sorted_note_designers


'''
    🧠 為什麼這樣寫更安全？
明確排除掉 None，避免 .lower() 報錯。
用 continue 直接略過不符合格式的資料。
若你想更保險，也可以改成：

if isinstance(nd, str) and keyword.lower() in nd.lower() and nd not in note_designers:
    note_designers.append(nd)

這樣不只排除 None，還能排除意外格式（例如 list、int）。
'''