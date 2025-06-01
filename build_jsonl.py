#!/usr/bin/env python3

import json, pathlib, re

REPO = "joshhuang0424/slide_writer_agent"
BRANCH = "main"
IMG_DIR = pathlib.Path("images")
JSON_DIR = pathlib.Path("json")
OUTFILE = "slides.jsonl"

def raw_url(file_path):
    return f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{file_path.as_posix()}"

rows = []
for img_path in IMG_DIR.glob("*.png"):
    slide_id = img_path.stem        # slide_0001
    json_path = JSON_DIR / f"{slide_id}.json"
    if not json_path.exists():
        print(f"[WARN] {slide_id} JSON 不存在，跳過")
        continue

    with open(json_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
        # 從 JSON 檔名中提取數字部分，並更新 meta 中的 slide_id
        slide_id_num = re.search(r'slide_(\d+)', slide_id).group(1)
        meta["slide_id"] = slide_id_num

    meta["image_url"] = raw_url(img_path)   # 動態加 URL
    rows.append(meta)

with open(OUTFILE, "w", encoding="utf-8") as f:
    for row in rows:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

print(f"✅ 產生 {OUTFILE}（{len(rows)} 列）")