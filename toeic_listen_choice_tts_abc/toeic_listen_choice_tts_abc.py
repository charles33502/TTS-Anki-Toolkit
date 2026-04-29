import asyncio
import csv
import html
import re
from pathlib import Path
import edge_tts

# ===== Settings =====
INPUT_FILE = "toeic_listen_questions_abc.txt"
OUTPUT_DIR = "toeic_listen_abc_output"
VOICE = "en-US-EmmaNeural"   # Example: en-US-GuyNeural
RATE = "+0%"                 # Example: "+10%" / "-10%"
PREFIX = "toeic"
START_INDEX = 1
SKIP_EXISTING_AUDIO = True

# Also create an Anki import TSV file.
GENERATE_TSV = True
TSV_FILENAME = "anki_import_abc.tsv"

# Add spoken labels before answer choices: "A...", "B...", "C..."
SPEAK_CHOICE_LABELS = True

# Use punctuation to make Edge TTS leave a short pause.
# Increase the number of dots if you want a longer pause.
LABEL_PAUSE = "..."
END_PAUSE = "..."

# Also create one combined audio file per question: Q + A + B + C, with pauses.
# The four separate audio files are still generated.
GENERATE_COMBINED_AUDIO = False
# ====================

CHOICE_LABELS = ["A", "B", "C"]
CHOICE_RE = re.compile(r"^\(?([ABCabc])\)?[\.\)]?\s*(.+)$")


def make_tts_text(part: str, text: str) -> str:
    text = text.strip()
    if part in CHOICE_LABELS and SPEAK_CHOICE_LABELS:
        return f"{part}. {LABEL_PAUSE} {text} {END_PAUSE}"
    return f"{text} {END_PAUSE}"


async def generate_tts(text: str, output_path: Path) -> None:
    communicate = edge_tts.Communicate(text=text, voice=VOICE, rate=RATE)
    await communicate.save(str(output_path))


def parse_one_block(block: str) -> dict:
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    if not lines:
        raise ValueError("Empty question block")

    result = {"Q": []}
    current = "Q"

    for line in lines:
        m = CHOICE_RE.match(line)
        if m:
            current = m.group(1).upper()
            result[current] = [m.group(2).strip()]
        else:
            result.setdefault(current, []).append(line)

    parsed = {k: " ".join(v).strip() for k, v in result.items()}
    required = ["Q"] + CHOICE_LABELS
    missing = [k for k in required if not parsed.get(k)]
    if missing:
        raise ValueError(f"Missing fields: {', '.join(missing)}\nRaw block:\n{block}")
    return parsed


def parse_input(text: str) -> list[dict]:
    blocks = re.split(r"^\s*---\s*$", text, flags=re.MULTILINE)
    return [parse_one_block(block) for block in blocks if block.strip()]


def sound_tag(filename: str) -> str:
    return f"[sound:{filename}]"


def make_anki_front(q_index: int) -> str:
    lines = [f"Q : {sound_tag(f'{PREFIX}_{q_index:03d}_Q.mp3')}"]
    for label in CHOICE_LABELS:
        lines.append(f"({label}) : {sound_tag(f'{PREFIX}_{q_index:03d}_{label}.mp3')}")
    return "<br>".join(lines)


def make_anki_back(item: dict) -> str:
    lines = [html.escape(item["Q"]), ""]
    for label in CHOICE_LABELS:
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

    for q_index, item in enumerate(questions, start=START_INDEX):
        for part in ["Q"] + CHOICE_LABELS:
            filename = f"{PREFIX}_{q_index:03d}_{part}.mp3"
            audio_path = output_dir / filename
            tts_text = make_tts_text(part, item[part])

            if SKIP_EXISTING_AUDIO and audio_path.exists():
                print(f"Skip existing: {filename}")
                skipped_count += 1
            else:
                print(f"Generate: {filename} <- {tts_text}")
                await generate_tts(tts_text, audio_path)
                generated_count += 1

        if GENERATE_COMBINED_AUDIO:
            combined_filename = f"{PREFIX}_{q_index:03d}_ALL.mp3"
            combined_path = output_dir / combined_filename
            combined_text = " ".join(make_tts_text(part, item[part]) for part in ["Q"] + CHOICE_LABELS)

            if SKIP_EXISTING_AUDIO and combined_path.exists():
                print(f"Skip existing: {combined_filename}")
                skipped_count += 1
            else:
                print(f"Generate: {combined_filename} <- {combined_text}")
                await generate_tts(combined_text, combined_path)
                generated_count += 1

    tsv_path = write_anki_tsv(questions, output_dir) if GENERATE_TSV else None

    print("\nDone.")
    print(f"Questions: {len(questions)}")
    print(f"Generated files: {generated_count}")
    print(f"Skipped files: {skipped_count}")
    print(f"Output folder: {output_dir.resolve()}")
    if tsv_path:
        print(f"Anki TSV: {tsv_path.resolve()}")


if __name__ == "__main__":
    asyncio.run(main())
