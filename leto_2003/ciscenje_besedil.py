import os
import re
from langdetect import detect

input_dir = "knjige_03_opisi"
output_dir = "03_ang_opisi"
log_file = "removed_log.txt"

os.makedirs(output_dir, exist_ok=True)

def is_mostly_english(text, threshold=0.9):
    # Najdemo vse besede, ki vsebujejo samo črke
    words = re.findall(r"\b[a-zA-Z]+\b", text)
    if not words:
        return False
    # Popravljeno: odstranjena odvečna poševnica pred narekovajem
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

with open(log_file, "w", encoding="utf-8") as log:
    for filename in os.listdir(input_dir):
        if not filename.endswith(".txt"):
            continue

        # Iskanje originalne številke (npr. 'knjiga_38.txt' -> '38')
        numbers = re.findall(r'\d+', filename)
        if numbers:
            original_id = numbers[0]
        else:
            original_id = filename.replace(".txt", "")

        path = os.path.join(input_dir, filename)

        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read().strip()
        except Exception as e:
            log.write(f"{filename} -> ERROR reading file: {e}\n")
            continue

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
            log.write(f"{filename} -> REMOVED: duplicate content\n")
            continue

        # Shranjevanje z ohranjenim originalnim ID-jem
        new_name = f"opis_{original_id}.txt"
        output_path = os.path.join(output_dir, new_name)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

        seen.add(norm)
        log.write(f"{filename} -> SAVED as {new_name}\n")

print("Preveri 'removed_log.txt' za podrobnosti.")