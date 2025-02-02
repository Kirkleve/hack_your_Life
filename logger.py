import logging

# ✅ Настраиваем логирование в `bot.log`
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


# ✅ Функции для логирования (чтобы код был чище)
def log_info(message):
    logging.info(message)


def log_warning(message):
    logging.warning(message)


def log_error(message):
    logging.error(message)


def log_critical(message):
    logging.critical(message)
