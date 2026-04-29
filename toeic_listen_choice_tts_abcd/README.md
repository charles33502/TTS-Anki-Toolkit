# TTS Anki Toolkit

A lightweight Python toolkit for generating language-learning audio files and Anki import TSV files using Microsoft Edge TTS.

這是一個用 Python 與 Microsoft Edge TTS 製作的語言學習輔助工具，可以把英文句子或 TOEIC 題型文字轉成 MP3 音檔，並產生可匯入 Anki 的 TSV 檔案。

This project is designed for Anki-based English listening, speaking, shadowing, and TOEIC-style practice workflows.

本專案主要用於 Anki 英文聽力、口說、跟讀練習，以及 TOEIC 類型題目的聽力訓練流程。

---

## Features / 功能特色

- Convert plain sentence lists into MP3 audio and Anki TSV files  
  將純文字句子列表轉換成 MP3 音檔與 Anki TSV 匯入檔

- Generate TOEIC-style listening cards with separate question and choice audio  
  產生 TOEIC 題型卡片，題目與各選項可分別產生音檔

- Supports ABC and ABCD choice formats  
  支援 A/B/C 三選項與 A/B/C/D 四選項格式

- Speaks choice labels such as "Letter A", "Letter B", and "Letter C"  
  可在選項音檔中念出「Letter A」、「Letter B」、「Letter C」等選項標籤

- Generates Anki-compatible TSV files  
  自動產生可匯入 Anki 的 TSV 檔案

- Windows `.bat` launchers for `.venv` workflows  
  提供適合 Windows `.venv` 虛擬環境使用的 `.bat` 執行檔

- Uses Microsoft Edge TTS via `edge-tts`  
  使用 `edge-tts` 串接 Microsoft Edge TTS 語音合成

---

## Project Structure / 專案結構

```txt
tts-anki-toolkit/
├─ README.md
├─ requirements.txt
├─ .gitignore
│
├─ TTS_to_anki_speaking/
│  ├─ batch_tts_to_anki.py
│  ├─ run_batch_tts_to_anki.bat
│  └─ sentences.txt
│
├─ toeic_listen_choice_tts_abc/
│  ├─ toeic_listen_choice_tts_abc.py
│  ├─ run_toeic_listen_choice_tts_abc.bat
│  └─ toeic_listen_questions_abc.txt
│
└─ toeic_listen_choice_tts_abcd/
   ├─ toeic_listen_choice_tts_abcd.py
   ├─ run_toeic_listen_choice_tts_abcd.bat
   └─ toeic_listen_questions_abcd.txt
```

---

## Tools / 工具說明

### 1. TTS to Anki Speaking / 句子轉語音 Anki 工具

This tool converts a plain sentence list into MP3 audio files and an Anki TSV import file.

這個工具會將一行一句的英文句子轉換成 MP3 音檔，並產生 Anki 可匯入的 TSV 檔案，適合用於聽力、口說、shadowing 跟讀練習。

Input format / 輸入格式：

```txt
Nvidia wasn't built overnight. It's taken us 33 years.
The first idea about Nvidia is that we're a full stack company.
```

Output / 輸出範例：

```txt
output_anki/
├─ anki_import.tsv
├─ Nvidia_001.mp3
├─ Nvidia_002.mp3
└─ ...
```

---

### 2. TOEIC Choice TTS ABC / TOEIC 三選項聽力工具

This tool generates separate audio files for TOEIC Part 2 style questions with A/B/C choices.

這個工具會針對 TOEIC Part 2 類型的三選項題目，分別產生題目與 A/B/C 選項的音檔，並產生 Anki TSV 匯入檔。

Input format / 輸入格式：

```txt
The company is planning to recruit more staff, isn't it?

(A) No, they're not included.
(B) Yes, two and a half will be enough.
(C) Absolutely, that's our top priority.
```

Output example / 輸出範例：

```txt
toeic_001_Q.mp3
toeic_001_A.mp3
toeic_001_B.mp3
toeic_001_C.mp3
anki_import_abc.tsv
```

---

### 3. TOEIC Choice TTS ABCD / TOEIC 四選項聽力工具

This tool generates separate audio files for four-choice listening questions.

這個工具會針對四選項聽力題，分別產生題目與 A/B/C/D 選項的音檔，並產生 Anki TSV 匯入檔。

Input format / 輸入格式：

```txt
Where is the orientation being held?

(A) In the main conference room.
(B) At the downtown hotel.
(C) Next Monday morning.
(D) By the human resources manager.
```

Output example / 輸出範例：

```txt
toeic_001_Q.mp3
toeic_001_A.mp3
toeic_001_B.mp3
toeic_001_C.mp3
toeic_001_D.mp3
anki_import_abcd.tsv
```

---

## Installation / 安裝方式

Create and activate a virtual environment:

建立並啟用 Python 虛擬環境：

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

安裝套件：

```bash
pip install -r requirements.txt
```

`requirements.txt`:

```txt
edge-tts
```

---

## Usage / 使用方式

Run a script directly:

可以直接執行 Python 腳本：

```bash
python TTS_to_anki_speaking/batch_tts_to_anki.py
```

Or double-click the corresponding `.bat` file on Windows.

也可以在 Windows 上直接雙擊對應的 `.bat` 檔案。

Example launchers / 執行檔範例：

```txt
run_batch_tts_to_anki.bat
run_toeic_listen_choice_tts_abc.bat
run_toeic_listen_choice_tts_abcd.bat
```

---

## Anki Import / Anki 匯入方式

Each tool generates an Anki-compatible TSV file.

每個工具都會產生可匯入 Anki 的 TSV 檔案。

Import the TSV into Anki and map the fields as follows:

將 TSV 匯入 Anki 時，欄位對應如下：

```txt
Field 1 -> Front
Field 2 -> Back
```

For TOEIC choice cards, the front side contains audio references:

TOEIC 題型卡片的正面會包含音檔引用：

```txt
Q : [sound:toeic_001_Q.mp3]
(A) : [sound:toeic_001_A.mp3]
(B) : [sound:toeic_001_B.mp3]
(C) : [sound:toeic_001_C.mp3]
```

The back side contains the original question and choices:

背面會顯示原始題目與選項文字：

```txt
The company is planning to recruit more staff, isn't it?

(A) No, they're not included.
(B) Yes, two and a half will be enough.
(C) Absolutely, that's our top priority.
```

Copy the generated MP3 files into Anki's `collection.media` folder if needed.

如果 Anki 無法直接播放音檔，請將產生的 MP3 檔案複製到 Anki 的 `collection.media` 資料夾。

---

## Input Notes / 輸入格式注意事項

Multiple questions can be separated by a line containing only `---`.

多題可以用只有 `---` 的一行分隔：

```txt
The company is planning to recruit more staff, isn't it?

(A) No, they're not included.
(B) Yes, two and a half will be enough.
(C) Absolutely, that's our top priority.

---

Where is the orientation being held?

(A) In the main conference room.
(B) At the downtown hotel.
(C) Next Monday morning.
(D) By the human resources manager.
```

Supported choice formats include:

支援的選項格式包括：

```txt
(A) text
A) text
A. text
A text
```

---

## Git Ignore / Git 忽略檔案建議

Generated files such as MP3 audio, TSV files, virtual environments, and personal question files should not be tracked by Git.

建議不要將虛擬環境、產生的音檔、TSV 檔案，以及個人題庫文字檔上傳到 GitHub。

Recommended `.gitignore`:

```gitignore
# Python
.venv/
__pycache__/
*.pyc

# Generated audio / Anki output
output/
output_anki/
toeic_listen_abc_output/
toeic_listen_abcd_output/
*.mp3
*.tsv

# Real input files
sentences.txt
toeic_listen_questions_abc.txt
toeic_listen_questions_abcd.txt

# OS / editor
.DS_Store
Thumbs.db
.vscode/
.idea/
```


---

## Motivation / 專案動機

This toolkit was built to reduce the friction between English practice materials, TTS audio generation, and Anki card creation.

這個工具的目標是降低英文練習材料、TTS 語音生成與 Anki 卡片製作之間的操作成本。

Instead of manually recording or editing audio files, learners can write plain text questions or sentences and automatically generate audio-based Anki cards.

使用者只需要準備純文字句子或題目，就可以自動產生音檔與 Anki 匯入檔，不需要手動錄音或逐一編輯音檔。