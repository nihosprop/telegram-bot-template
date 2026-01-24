## `Project structure`

```text
Stepik-Mentor-Metric/
├── src/
│   ├── main.py             # Application entry point
│   ├── bot/                # Telegram bot logic (aiogram)
│   │   ├── dialogs/        # Сценарии диалогов (aiogram_dialog)
│   │   ├── factory/        # Фабрики callback-данных
│   │   ├── middlewares/    # Промежуточные слои (логирование, сессии БД)
│   │   └── states/         # States
│   ├── common/             # General utilitie
│   ├── core/               # Настройки (Pydantic) и константы
│   ├── db/                 # Работа с базой данных (SQLAlchemy)
│   │   ├── models/         # Описание таблиц
│   │   └── repository/     # CRUD operations
│   ├── services/           # Интеграция со Stepik API
│   └── tasks/              # Фоновые задачи (планировщик)
├── tests/                  # Tests
├── Dockerfile              # Instructions for assembling the container
├── docker-compose.yml      # 
├── pyproject.toml          # Project Dependencies
└── .env.example            # Example environment variables