from typing import Optional


def parse_context_string(context_str: str) -> dict:
    context = {}
    if not context_str:
        return context

    parts = [p.strip() for p in context_str.split(',')]

    for part in parts:
        if '=' in part:
            key, value = part.split('=', 1)
            context[key.strip()] = value.strip()
        else:
            context['topic'] = part

    return context


def validate_context(context: dict, required_keys: list) -> bool:
    return all(key in context for key in required_keys)
