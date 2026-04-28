# Telegram Bot Template

A template for building Telegram bots in Python using **aiogram 3.x**, **aiogram-dialog**, and a modern technology stack.

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | [aiogram](https://github.com/aiogram/aiogram) 3.x |
| Dialogs | [aiogram-dialog](https://github.com/Tishka17/aiogram_dialog) |
| DI Container | [dishka](https://github.com/reagento/dishka) |
| Database | PostgreSQL + SQLAlchemy 2.x (async) |
| ORM | SQLAlchemy 2.x |
| FSM Storage | Redis |
| Task Scheduler | TaskIQ + PostgreSQL + Redis |
| Configuration | Dynaconf |
| Linter/Formatter | Ruff |
| Type Checker | Ty |

---

## Quick Start

### 1. Clone and Setup

```bash
git clone <repo-url>
cd telegram-bot-template

# Create .env file based on the example below
touch .env
```

### 2. Environment Variables (.env)

```bash
# Bot
BOT_TOKEN=your_telegram_bot_token
BOT_ADMINS=123456789 987654321  # Admin IDs separated by space

# Postgres
POSTGRES_DB=bot_db
POSTGRES_USER=bot_user
POSTGRES_PASSWORD=secure_password_min_7_chars
POSTGRES_HOST=postgres_db

# Redis
REDIS_HOST=redis
REDIS_PASSWORD=redis_password_min_7_chars

# Environment
ENV_FOR_DYNACONF=production  # or default
```

### 3. Run with Docker Compose

```bash
docker compose up -d
```

### 4. Local Development (without Docker)

```bash
# Install dependencies
pip install -e .

# Run
python src/main.py
```

---

## Project Structure

```
telegram-bot-template/
├── src/
│   ├── main.py                 # Application entry point
│   ├── bot/
│   │   ├── dialogs/            # aiogram-dialog dialogs
│   │   │   ├── flows/          # Dialog flows
│   │   │   │   └── start/      # Start dialog
│   │   │   │       ├── dialog.py      # Window definitions
│   │   │   │       ├── handlers.py    # Command handlers
│   │   │   │       └── states.py      # Dialog states
│   │   │   └── common/         # Common components
│   │   ├── middlewares/        # Middleware (ACL, logging)
│   │   └── commands.py         # Menu commands setup
│   ├── core/
│   │   ├── main_config.py      # Pydantic configuration
│   │   ├── logger.py           # Logging setup
│   │   └── enum.py             # Enums (roles)
│   ├── db/
│   │   ├── models/             # SQLAlchemy models
│   │   └── repository/         # Repositories (CRUD)
│   ├── infrastructure/
│   │   └── di/                 # dishka DI providers
│   │       └── providers/      # Bot, DB, Redis, Repositories
│   ├── services/               # Business logic
│   └── tasks/                  # TaskIQ background tasks
│       ├── broker.py           # Redis broker setup
│       ├── scheduler.py        # Scheduler
│       └── tasks.py            # Task definitions
├── settings.toml               # Dynaconf configuration
├── docker-compose.yml          # Infrastructure
└── Dockerfile                  # Image build
```

---

## Key Components

### DI (Dependency Injection)

The project uses **dishka** for dependency injection:

- `ConfigProvider` — configuration
- `PostgresProvider` — DB sessions (Scope.REQUEST)
- `RedisProvider` — Redis connection
- `RepositoryProvider` — repositories
- `BotProvider` — bot instance

Example usage in a handler:

```python
from dishka.integrations.aiogram import inject
from aiogram_dialog import DialogManager

@inject
async def my_handler(
    message: Message,
    dialog_manager: DialogManager,
    user_repo: FromDishka[UserRepository],
) -> None:
    user = await user_repo.get_by_id(message.from_user.id)
```

### Dialogs (aiogram-dialog)

Dialogs are located in `src/bot/dialogs/flows/`:

```python
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

my_dialog = Dialog(
    Window(
        Const("Hello!"),
        Start(Const("Next"), id="next", state=NextSG.start),
        state=MySG.start,
    ),
)
```

### ACL Middleware

`ACLMiddleware` handles access control:
- Super admins (from `BOT_ADMINS`) — full access
- Regular users — checked against DB (`is_active`, `role`)
- Inactive users — access denied

### Background Tasks (TaskIQ)

Tasks are defined in `src/tasks/tasks.py`:

```python
@broker.task
@inject(patch_module=True)
async def send_notification(
    bot: FromDishka[Bot],
    user_id: int,
) -> None:
    await bot.send_message(user_id, "Notification!")
```

Run worker:
```bash
python -m taskiq worker tasks.broker:broker --fs-discover
```

Run scheduler:
```bash
python -m taskiq scheduler tasks.scheduler:scheduler --fs-discover
```

---

## User Roles

| Role | Description |
|------|-------------|
| `super_admin` | Full access, set via `BOT_ADMINS` |
| `admin` | Extended rights, set in DB |

---

## Database Migrations

The project uses Alembic for database migrations.

### Using migrate.sh (Recommended)

The `migrate.sh` script automates migration creation with testing:

```bash
# Create and test migration
./migrate.sh "add_users_table"
```

What the script does:
1. Starts PostgreSQL container
2. Generates migration file (`alembic revision --autogenerate`)
3. **Test drive**: upgrade → downgrade → upgrade
4. Checks model/database consistency
5. Stops the container

### Manual Migration Commands

```bash
# Locally
cd src
alembic revision --autogenerate -m "description"
alembic upgrade head

# In Docker (runs automatically on startup)
docker compose run --rm migrations
```

---

## Linting and Formatting

```bash
# Check
ruff check src

# Auto-fix
ruff check --fix src

# Format
ruff format src
```

## Type Checking

```bash
# Run Ty type checker
python -m ty src
```

---

## Requirements

- Python 3.14+
- PostgreSQL 18+
- Redis 8+

---

## License

MIT License