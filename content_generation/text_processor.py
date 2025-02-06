def split_text_by_paragraphs(text, max_length=1024):
    """✂️ Разделение текста на заголовок и основную часть с учётом ограничения длины."""
    paragraphs = text.split('\n')  # Разделяем текст по абзацам
    if not paragraphs:
        return "", [""]  # Если нет текста, возвращаем пустые значения

    title = paragraphs[0]  # 🏆 Первый абзац — заголовок
    body = "\n".join(paragraphs[1:]).strip()  # Остальной текст

    # 🔹 Разбиваем основную часть на блоки (по 1024 символа)
    messages = []
    current_message = ""

    for paragraph in body.split('\n'):
        if len(current_message) + len(paragraph) + 1 <= max_length:
            current_message += (paragraph + "\n")
        else:
            messages.append(current_message.strip())
            current_message = paragraph + "\n"

    # Добавляем последний кусок текста
    if current_message.strip():
        messages.append(current_message.strip())

    return title, messages  # ✅ Заголовок + список частей основного текста
