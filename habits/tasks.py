import requests


def send_telegram_message(chat_id, message):
    """
    Отправляет сообщение в Telegram через Telegram Bot API.

    Args:
        chat_id (int or str): Идентификатор чата или имя пользователя, куда нужно отправить сообщение.
        message (str): Текст сообщения, которое нужно отправить. Поддерживаются HTML и Markdown для форматирования.

    Returns:
        str: Результат выполнения операции. Сообщение об успешной отправке или сообщение об ошибке с текстом ответа от сервера.

    Пример использования:
        send_telegram_message(chat_id=123456789, message="Привет, это тестовое сообщение!")

    Исключения:
        - В случае успешной отправки возвращается строка с подтверждением отправки сообщения.
        - В случае ошибки возвращается текст ошибки от API Telegram.

    Примечания:
        - `token`: Токен вашего Telegram-бота. Его необходимо заменить на реальный.
        - `parse_mode`: Можно использовать значения "HTML" или "Markdown", чтобы форматировать текст сообщения. Например, для жирного текста можно использовать теги HTML: `<b>текст</b>`.
    """
    token = "YOUR_TELEGRAM_BOT_TOKEN"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",  # Можно использовать HTML или Markdown для форматирования текста
    }
    response = requests.post(url, data=payload)

    if response.status_code == 200:
        return f"Сообщение отправлено: {message}"
    else:
        return f"Ошибка отправки сообщения: {response.text}"
