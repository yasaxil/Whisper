
# Whisper GUI 3.0

## Описание

Whisper GUI 3.0 - это инструмент для автоматической обработки аудио и видео файлов с использованием модели автоматического распознавания речи от OpenAI (Whisper). Скрипт предоставляет графический интерфейс на базе Streamlit, позволяющий пользователям легко выбирать директории для обработки файлов и отслеживать прогресс обработки в реальном времени.

## Функционал

- **Поддержка аудио и видео файлов**: Скрипт может обрабатывать файлы с расширениями `.ogg` и `.mp4`.
- **Извлечение аудио из видео**: Для видео файлов аудио дорожка извлекается перед обработкой.
- **Конвертация в текст**: Аудио файлы конвертируются в текст с помощью модели Whisper.
- **Логирование**: Все операции записываются в лог, который сохраняется в директории обработанных файлов.
- **Прогресс обработки**: Прогресс обработки отображается в реальном времени через интерфейс Streamlit.
- **Проверка доступности директорий**: Скрипт проверяет, что указанная директория существует и доступна для чтения.

## Требования

Для работы скрипта необходимы следующие библиотеки:
- Python 3.8+
- moviepy
- pydub
- transformers
- streamlit

## Установка

Установите необходимые зависимости с помощью pip:

```bash
pip install moviepy pydub transformers streamlit
```

## Использование

1. Запустите Streamlit интерфейс:

```bash
streamlit whisper 3.0.py
```

2. Введите путь к директории, содержащей файлы для обработки.
3. Нажмите кнопку "Начать обработку" для запуска процесса.
4. Дождитесь завершения обработки и проверьте логи и результаты в указанной директории.

## Логирование 

В этом коде функция setup_logging теперь непосредственно создаёт файл лога в выходной директории, что позволяет легко отслеживать процесс обработки файлов в выбранной директории.


