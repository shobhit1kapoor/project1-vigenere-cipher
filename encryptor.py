#!/usr/bin/env python3
"""Line-oriented Vigenere cipher process used by the driver."""

import re
import sys


LETTERS_ONLY = re.compile(r"[A-Za-z]+\Z")


def is_letters_only(value):
    return bool(LETTERS_ONLY.fullmatch(value))


def vigenere(text, key, decrypt=False):
    """Transform uppercase A-Z text with a repeating Vigenere key."""
    result = []
    direction = -1 if decrypt else 1

    for index, character in enumerate(text):
        text_value = ord(character) - ord("A")
        key_value = ord(key[index % len(key)]) - ord("A")
        result.append(chr(((text_value + direction * key_value) % 26) + ord("A")))

    return "".join(result)


def handle_command(line, current_key):
    """Return (response, updated_key, should_quit) for one input line."""
    parts = line.rstrip("\r\n").split(maxsplit=1)
    if not parts:
        return "ERROR Empty command", current_key, False

    command = parts[0].upper()
    argument = parts[1] if len(parts) == 2 else ""

    if command == "QUIT":
        return None, current_key, True

    if command == "PASS":
        if not is_letters_only(argument):
            return "ERROR Passkey must contain only letters", current_key, False
        return "RESULT", argument.upper(), False

    if command in ("ENCRYPT", "DECRYPT"):
        if current_key is None:
            return "ERROR Password not set", current_key, False
        if not is_letters_only(argument):
            return "ERROR Input must contain only letters", current_key, False

        transformed = vigenere(
            argument.upper(), current_key, decrypt=(command == "DECRYPT")
        )
        return "RESULT " + transformed, current_key, False

    return "ERROR Unknown command", current_key, False


def run():
    current_key = None

    for line in sys.stdin:
        response, current_key, should_quit = handle_command(line, current_key)
        if should_quit:
            break
        print(response, flush=True)


if __name__ == "__main__":
    run()
