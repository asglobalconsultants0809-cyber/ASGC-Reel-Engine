import textwrap


def clean_text(value):
    if value is None:
        return ""
    return str(value).strip()


def limit_list(items, max_items=5):
    if not isinstance(items, list):
        return []
    return items[:max_items]


def wrap_text(text, width=42):
    if not text:
        return []
    return textwrap.wrap(str(text), width=width)