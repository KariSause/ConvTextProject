# Call QA Automation System

## 📌 Опис

Система автоматизує контроль якості дзвінків:
- Завантажує аудіофайли дзвінків з Google Drive
- Транскрибує аудіо за допомогою локального Whisper
- Аналізує якість менеджера (через GPT або локальний аналіз)
- Заповнює Excel-таблицю результатами, виставляє оцінки та підсвічує проблемні дзвінки

---

## Як почати налаштувати проєкт?

### 1. Клонуйте репозиторій та перейдіть у папку проекту

```powershell
git clone <URL-репозиторію>
cd ConvTextProject
```

### 2. Створіть та активуйте віртуальне середовище (venv)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Встановіть залежності

```powershell
pip install -r requirements.txt
```

### 4. Налаштуйте змінні середовища

- Скопіюйте `.env.example` у `.env` і заповніть:
  - `service_account.json` — для доступу до Google Drive/Sheets через OAuth
  - Інші змінні — див. коментарі у `.env.example`

### 5. Встановіть ffmpeg (для Whisper)

- [Завантажити ffmpeg](https://ffmpeg.org/download.html) і додати шлях до ffmpeg.exe у змінну середовища `PATH`.

### 6. Запустіть основний скрипт

```powershell
python scripts/main.py
```

---

## 🗂️ Структура проекту

- `scripts/drive.py` — робота з Google Drive (завантаження/вивантаження файлів)
- `scripts/transcription.py` — транскрипція аудіо через Whisper
- `scripts/excel_processor.py` — обробка та оновлення Excel-таблиці
- `scripts/main.py` — основний оркестратор
- `requirements.txt` — залежності
- `.env.example` — приклад змінних середовища

---


## 📝 Змінні середовища

Всі налаштування зберігаються у файлі `.env` (створіть його на основі `.env.example`). Нижче — пояснення для кожної змінної:

| Змінна                  | Опис                                      |
|-------------------------|--------------------------------------------|
| SOURCE_FOLDER_ID        | ID папки Google Drive, звідки завантажуються аудіофайли (наприклад, "1a2b3c...") |
| TARGET_FOLDER_ID        | ID папки Google Drive, куди можна завантажувати результати (опціонально) |
| SOURCE_SHEET_ID         | ID Google Sheets (Excel-файлу), куди записуються результати (наприклад, "1a2b3c...") |
| OPENAI_API_KEY          | Ключ OpenAI для GPT-аналізу (опціонально, якщо не використовується — залиште порожнім) |

А також окремо необхідний `service_account.json` його можна отримати в Google Console.

**Як отримати ці значення:**
- `SOURCE_FOLDER_ID`, `TARGET_FOLDER_ID` — відкрийте потрібну папку в Google Drive, скопіюйте ID з URL.
- `SOURCE_SHEET_ID` — відкрийте Google Sheet, скопіюйте ID з URL.
- `OPENAI_API_KEY` — згенеруйте ключ у [OpenAI](https://platform.openai.com/account/api-keys), якщо потрібно.


---

## Важливі нюанси

- Всі аудіофайли завантажуються у `data/audio/`.
- Транскрипти зберігаються у `data/transcripts/`.
- Для коректної роботи Whisper потрібен ffmpeg.
- Для доступу до Google Drive/Sheets використовуйте OAuth (не сервісний акаунт).
- Всі змінні середовища мають бути заповнені!

---

## Як запустити, коли все налаштовано

```powershell
# Активація venv
.\venv\Scripts\Activate.ps1

# Встановлення залежностей
pip install -r requirements.txt

# Запуск основного процесу
python scripts/main.py
```

---
