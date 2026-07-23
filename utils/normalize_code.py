"""Normalize a raw string into a canonical 10-digit code."""

import string

MAX_LENGTH = 10
_ASCII_DIGITS = set(string.digits)


def normalize_code(raw: str | None) -> str:
    """Normalize `raw` into a canonical 10-digit numeric code string.

    Rules:
        1. Leading/trailing whitespace is trimmed.
        2. A single leading "N"/"n" prefix is stripped (any other leading
           letter is invalid).
        3. What remains must be non-empty, all digits, and at most 10
           characters long.
        4. The result is left-padded with zeros to exactly 10 digits.

    Raises:
        ValueError: if `raw` is None or cannot be normalized per the rules
            above.
    """
    if raw is None:
        raise ValueError("Raw cannot be None.")

    trimmed = raw.strip()
    if not trimmed:
        raise ValueError("Raw cannot be empty.")

    if trimmed[0] in ("N", "n"):
        body = trimmed[1:]
    elif trimmed[0].isalpha():
        raise ValueError(
            f"Invalid leading letter {trimmed[0]!r}; only 'N'/'n' is allowed."
        )
    else:
        body = trimmed

    if not body:
        raise ValueError("Code has no digits after the prefix was stripped.")

    if not all(ch in _ASCII_DIGITS for ch in body):
        raise ValueError(f"Code must be all digits, got {body!r}.")

    if len(body) > MAX_LENGTH:
        raise ValueError(
            f"Code has {len(body)} digits; at most {MAX_LENGTH} are allowed."
        )

    return body.zfill(MAX_LENGTH)