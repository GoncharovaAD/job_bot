# 🌩️ JobStormBot v2

Telegram-бот для поиска вакансий под профиль:

- Technical Writing — Middle/Senior
- Junior tech roles
- Meteorology / weather / climate — отдельный приоритет
- Europe / European remote
- Python, SQL, REST, OpenAPI, Postman, JSON
- PostgreSQL, DBeaver
- Git, GitHub Actions, Linux, Bash, PowerShell
- MkDocs, Markdown, Docs-as-Code
- HTML, CSS, JavaScript

## Быстрый запуск

### 1. Создай Telegram-бота

В Telegram открой `@BotFather`, создай бота через `/newbot` и получи token.

### 2. Создай окружение

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Создай `.env`

Скопируй `.env.example` в `.env`:

```text
BOT_TOKEN=твой_токен
CHECK_INTERVAL_MINUTES=30
MAX_JOBS_PER_CHECK=10
```

### 4. Запусти

```bash
python bot.py
```

### 5. В Telegram

Открой своего бота:

```text
/start
```

Полезные команды:

```text
/profile
/settings
/jobs
/help
```

## Важное ограничение v2

Сейчас источник вакансий — Arbeitnow. Это сделано намеренно: сначала стабилизируем профиль и matching, затем добавляем дополнительные источники.

Также текущий matching эвристический, а не LLM-based. Он объяснимый и быстрый, но не понимает вакансию так хорошо, как полноценный семантический анализ.

Следующий логичный апгрейд:

1. несколько job sources;
2. AI matching вакансии ↔ CV;
3. зарплата и валюта;
4. country/visa/work-permit filters;
5. saved / rejected вакансии;
6. feedback loop;
7. ежедневный digest;
8. отдельный `🌦️ Weather Radar` режим.
