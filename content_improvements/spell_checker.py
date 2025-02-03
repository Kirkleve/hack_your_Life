import language_tool_python

tool = language_tool_python.LanguageTool("ru")

def correct_text(text):
    """🔍 Проверяет и исправляет ошибки в тексте."""
    return tool.correct(text)
