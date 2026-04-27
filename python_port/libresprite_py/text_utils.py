"""Python port of selected text helpers from `src/base/*_string.cpp`."""

from __future__ import annotations


def replace_string(subject: str, replace_this: str, with_that: str) -> str:
    """Port of base::replace_string preserving left-to-right replacement semantics."""
    if replace_this == "":
        return subject

    i = 0
    out = subject
    while True:
        i = out.find(replace_this, i)
        if i == -1:
            break
        out = out[:i] + with_that + out[i + len(replace_this) :]
        i += len(with_that)
    return out


def split_string(value: str, separators: str) -> list[str]:
    """Port of base::split_string; keeps empty segments like the C++ version."""
    parts: list[str] = []
    beg = 0
    while True:
        positions = [value.find(sep, beg) for sep in separators]
        positions = [pos for pos in positions if pos != -1]
        end = min(positions) if positions else -1
        if end != -1:
            parts.append(value[beg:end])
            beg = end + 1
        else:
            parts.append(value[beg:])
            break
    return parts


def trim_string(value: str) -> str:
    """Faithful port of base::trim_string from C++ (including edge-case behavior)."""
    i = 0
    size = len(value)
    while i < size:
        if not value[i].isspace():
            break
        i += 1

    j = size - 1
    while j > i:
        if not value[j].isspace():
            break
        j -= 1

    if i < j:
        return value[i : j + 1]
    return ""
