import asyncio
import csv
import html
import re
from pathlib import Path
import edge_tts

# ===== Settings =====
INPUT_FILE = "toeic_listen_questions_abcd.txt"
OUTPUT_DIR = "toeic_listen_abcd_output"
VOICE = "en-US-EmmaNeural"   # e.g. en-US-GuyNeural
RATE = "+0%"                 # e.g. "+10%" / "-10%"
PREFIX = "toeic"
START_INDEX = 1
SKIP_EXISTING_AUDIO = False   # While testing, keep False so old files are overwritten

# Also create an Anki import TSV file.
GENERATE_TSV = True
TSV_FILENAME = "anki_import_abcd.tsv"

# Choose which labels your questions use.
# For TOEIC Part 2, use ["A", "B", "C"].
# For 4-option questions, use ["A", "B", "C", "D"].
CHOICE_LABELS = ["A", "B", "C", "D"]

# How to speak labels: "Letter" -> "Letter A." / "Raw" -> "A."
CHOICE_LABEL_STYLE = "Letter"
LABEL_PAUSE_TEXT = "..."
END_PAUSE_TEXT = "..."
# ====================

# Accepts formats like:
# (A) text
# A) text
# A. text
# A text
CHOICE_RE = re.compile(r"^\(?([A-Z])\)?[\.)]?\s*(.+)$", re.IGNORECASE)


def speak_text_for_part(part: str, text: str) -> str:
    """Add spoken labels and pauses for choices."""
    if part == "Q":
        return f"{text} {END_PAUSE_TEXT}".strip()

    if CHOICE_LABEL_STYLE.lower() == "letter":
        label = f"Letter {part}."
    else:
        label = f"{part}."

    return f"{label} {LABEL_PAUSE_TEXT} {text} {END_PAUSE_TEXT}".strip()


async def generate_tts(text: str, output_path: Path) -> None:
    communicate = edge_tts.Communicate(text=text, voice=VOICE, rate=RATE)
    await communicate.save(str(output_path))


def parse_one_block(block: str) -> dict:
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    if not lines:
        raise ValueError("Empty question block")

    result = {"Q": []}
    current = "Q"
    valid_choices = set(label.upper() for label in CHOICE_LABELS)

    for line in lines:
        m = CHOICE_RE.match(line)
        if m and m.group(1).upper() in valid_choices:
            current = m.group(1).upper()
            result[current] = [m.group(2).strip()]
        else:
            result.setdefault(current, []).append(line)

    parsed = {k: " ".join(v).strip() for k, v in result.items()}

    required = ["Q"] + [label.upper() for label in CHOICE_LABELS]
    missing = [k for k in required if not parsed.get(k)]
    if missing:
        raise ValueError(f"Missing fields: {', '.join(missing)}\nOriginal block:\n{block}")

    return parsed


def parse_input(text: str) -> list[dict]:
    # Separate multiple questions with a line containing only ---
    blocks = re.split(r"^\s*---\s*$", text, flags=re.MULTILINE)
    return [parse_one_block(block) for block in blocks if block.strip()]


def sound_tag(filename: str) -> str:
    return f"[sound:{filename}]"


def make_anki_front(q_index: int) -> str:
    """Front field: audio only, using Anki sound tags and HTML line breaks."""
    lines = [f"Q : {sound_tag(f'{PREFIX}_{q_index:03d}_Q.mp3')}"]
    for label in [label.upper() for label in CHOICE_LABELS]:
        lines.append(f"({label}) : {sound_tag(f'{PREFIX}_{q_index:03d}_{label}.mp3')}")
    return "<br>".join(lines)


def make_anki_back(item: dict) -> str:
    """Back field: original text answer, using HTML line breaks."""
    lines = [html.escape(item["Q"]), ""]
    for label in [label.upper() for label in CHOICE_LABELS]:
        lines.append(f"({label}) {html.escape(item[label])}")
    return "<br>".join(lines)


def write_anki_tsv(questions: list[dict], output_dir: Path) -> Path:
    tsv_path = output_dir / TSV_FILENAME
    with tsv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        for q_index, item in enumerate(questions, start=START_INDEX):
            writer.writerow([make_anki_front(q_index), make_anki_back(item)])
    return tsv_path


async def main() -> None:
    input_path = Path(INPUT_FILE)
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    questions = parse_input(input_path.read_text(encoding="utf-8"))
    generated_count = 0
    skipped_count = 0

    parts = ["Q"] + [label.upper() for label in CHOICE_LABELS]

    for q_index, item in enumerate(questions, start=START_INDEX):
        for part in parts:
            filename = f"{PREFIX}_{q_index:03d}_{part}.mp3"
            audio_path = output_dir / filename
            tts_text = speak_text_for_part(part, item[part])

            if SKIP_EXISTING_AUDIO and audio_path.exists():
                print(f"Skip existing: {filename}")
                skipped_count += 1
            else:
                print(f"Generate: {filename} <- {tts_text}")
                await generate_tts(tts_text, audio_path)
                generated_count += 1

    tsv_path = write_anki_tsv(questions, output_dir) if GENERATE_TSV else None

    print("\nDone.")
    print(f"Questions: {len(questions)}")
    print(f"Generated: {generated_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Output folder: {output_dir.resolve()}")
    if tsv_path:
        print(f"Anki TSV: {tsv_path.resolve()}")


if __name__ == "__main__":
    asyncio.run(main())
