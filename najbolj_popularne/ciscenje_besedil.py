import os
import re
from langdetect import detect

input_dir = "najboljse_knjige_opisi"
output_dir = "naj_ang_opisi"
log_file = "removed_log.txt"

os.makedirs(output_dir, exist_ok=True)

def is_mostly_english(text, threshold=0.9):
    words = re.findall(r"\b[a-zA-Z]+\b", text)
    if not words:
        return False
    english_like = sum(1 for w in words if re.match(r"^[a-zA-Z]+$", w))
    return (english_like / len(words)) >= threshold

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def normalize(text):
    return " ".join(text.lower().split())

seen = set()
count = 0

with open(log_file, "w", encoding="utf-8") as log:
    for filename in os.listdir(input_dir):
        if not filename.endswith(".txt"):
            continue

        path = os.path.join(input_dir, filename)

        with open(path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        if not text:
            log.write(f"{filename} -> REMOVED: empty\n")
            continue

        lang = detect_language(text)

        if lang != 'en':
            log.write(f"{filename} -> REMOVED: language={lang}\n")
            continue

        if not is_mostly_english(text):
            log.write(f"{filename} -> REMOVED: low English ratio\n")
            continue

        norm = normalize(text)

        if norm in seen:
            log.write(f"{filename} -> REMOVED: duplicate\n")
            continue

        seen.add(norm)

        new_filename = f"opis_{count+1}.txt"
        new_path = os.path.join(output_dir, new_filename)

        with open(new_path, "w", encoding="utf-8") as f:
            f.write(text)

        count += 1

print("Število ohranjenih opisov:", count)
print("Log zapisan v:", log_file)