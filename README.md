project/
│   main.py  # Основной файл для запуска бота
│   config.py  # Файл с настройками и переменными окружения
│   logging_config.py  # Конфигурация логирования
│   requirements.txt  # Список зависимостей
│   Dockerfile  # Конфигурация Docker-образа
│   docker-compose.yml  # Конфигурация Docker Compose
│   .gitlab-ci.yml  # Конфигурация CI/CD в GitLab
│
├── bot/
│   ├── __init__.py
│   ├── handlers.py  # Обработчики команд и сообщений
│   ├── admin.py  # Административные команды и функционал
│   ├── database.py  # Работа с базой данных
│   ├── utils.py  # Вспомогательные функции
│
├── data/
│   ├── __init__.py
│   ├── question.py  # Файл с вопросами
│
├── logs/
│   ├── bot.log  # Логи работы бота
│