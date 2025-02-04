import language_tool_python
from logger import log_info, log_error

# 🛠 Создаём один объект LanguageTool (оптимизация)
tool = language_tool_python.LanguageTool("ru")

# 🔍 Список терминов, которые НЕ нужно исправлять
EXCLUDED_TERMS = {"биохакинг", "нейропластичность", "митохондрии", "адаптогены", "дофамин", "серотонин", "нейротрансмиттер"}

def correct_text(text):
    """🔍 Проверяет и исправляет ошибки в тексте, но НЕ исправляет термины из списка EXCLUDED_TERMS."""
    try:
        matches = tool.check(text)
        for match in matches:
            if any(term in match.context for term in EXCLUDED_TERMS):
                continue  # Пропускаем исправления для специфических терминов
            text = text.replace(match.context, match.replacements[0] if match.replacements else match.context)
        log_info("✅ Орфография проверена успешно.")
        return text
    except Exception as e:
        log_error(f"❌ Ошибка при проверке орфографии: {e}")
        return text  # Если ошибка, возвращаем оригинальный текст
