import logging

# Создаем функцию для конфигурации логгера
def setup_logger():
    logging.basicConfig(
        format='[%(asctime)s] %(message)s',  # Формат сообщения
        datefmt='%Y-%m-%d %H:%M:%S',         # Формат даты и времени
        level=logging.INFO                     # Уровень логирования
    )
    return logging.getLogger()

logger = setup_logger()