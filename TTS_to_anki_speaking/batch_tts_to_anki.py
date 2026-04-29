import asyncio
from pathlib import Path
import edge_tts

# ===== 設定區 =====
INPUT_FILE = "sentences.txt"
OUTPUT_DIR = "output_anki"
VOICE = "en-US-EmmaNeural"   # 可改
RATE = "+0%"                 # 例如 "+10%" / "-10%"
PREFIX = "Nvidia"                # 音檔前綴，例如 "cs" 會產生 cs_001.mp3, cs_002.mp3 ...
START_INDEX = 1
SKIP_EXISTING_AUDIO = True   # 是否跳過已存在的音檔
# =================

async def generate_tts(text: str, output_path: Path) -> None:
    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate=RATE,
    )
    await communicate.save(str(output_path))

async def main():
    input_path = Path(INPUT_FILE)
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f"找不到輸入檔：{INPUT_FILE}")

    lines = input_path.read_text(encoding="utf-8").splitlines()
    sentences = [line.strip() for line in lines if line.strip()]

    if not sentences:
        raise ValueError("沒有可處理的句子。")

    tsv_path = output_dir / "anki_import.tsv"

    generated_count = 0
    skipped_count = 0

    with tsv_path.open("w", encoding="utf-8", newline="") as f:
        for i, sentence in enumerate(sentences, start=START_INDEX):
            filename = f"{PREFIX}_{i:03d}.mp3"
            audio_path = output_dir / filename

            if SKIP_EXISTING_AUDIO and audio_path.exists():
                print(f"跳過既有音檔：{filename}")
                skipped_count += 1
            else:
                print(f"生成音檔：{filename}")
                await generate_tts(sentence, audio_path)
                generated_count += 1

            front = f"[sound:{filename}]"
            back = sentence
            f.write(f"{front}\t{back}\n")

    print("\n完成。")
    print(f"新生成音檔：{generated_count}")
    print(f"跳過既有音檔：{skipped_count}")
    print(f"音檔資料夾：{output_dir.resolve()}")
    print(f"TSV 檔案：{tsv_path.resolve()}")

if __name__ == "__main__":
    asyncio.run(main())