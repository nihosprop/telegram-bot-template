import re


def check_tg_user_id(text: str) -> str:
    """
    Checks if the input string is a valid Telegram user ID.

    Args:
        text (str): The input string to be validated.
    Returns:
        str: The input string if it is a valid Telegram user ID.
    Raises:
        ValueError: If the input string is not a valid Telegram user ID.
    """
    cleaned_text = text.strip()

    if cleaned_text.isdecimal() and int(cleaned_text) >= 10000:
        return cleaned_text
    raise ValueError
