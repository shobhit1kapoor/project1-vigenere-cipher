#!/usr/bin/env python3
"""Driver draft with a session history and history/new-value menus."""
import os
import subprocess
import sys


def choose(history, purpose):
    choice = input("Use [n]ew or [h]istory for {}? ".format(purpose)).strip().lower()
    if choice.startswith("h") and history:
        for number, item in enumerate(history, start=1):
            print("{}. {}".format(number, item))
        while True:
            selected = input("Number, n for new, or q to cancel: ").strip().lower()
            if selected == "q":
                return None, False
            if selected == "n":
                return input("New {}: ".format(purpose)), True
            if selected.isdigit() and 1 <= int(selected) <= len(history):
                return history[int(selected) - 1], False
            print("Choose a listed number, n, or q.")
    if choice.startswith("h"):
        print("History is empty; enter n for a new value or q to cancel.")
        if input("Choice: ").strip().lower() == "q":
            return None, False
    elif choice.startswith("q"):
        return None, False
    return input("New {}: ".format(purpose)), True


def main():
    if len(sys.argv) != 2:
        print("Usage: python driver.py LOG_FILE")
        return 2
    folder = os.path.dirname(os.path.abspath(__file__))
    logger = subprocess.Popen([sys.executable, os.path.join(folder, "logger.py"), sys.argv[1]],
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              text=True, encoding="utf-8", bufsize=1)
    cipher = subprocess.Popen([sys.executable, os.path.join(folder, "encryptor.py")],
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              text=True, encoding="utf-8", bufsize=1)
    history = []
    print("Commands: password, encrypt, decrypt, history, quit")

    while True:
        command = input("command> ").strip().lower()
        if command == "quit":
            break
        if command == "history":
            for number, item in enumerate(history, start=1):
                print("{}. {}".format(number, item))
            continue
        if command not in ("password", "encrypt", "decrypt"):
            print("Unknown command.")
            continue

        value, is_new = choose(history, command)
        if value is None:
            continue
        if command != "password" and is_new:
            history.append(value)
        protocol = "PASS" if command == "password" else command.upper()
        cipher.stdin.write("{} {}\n".format(protocol, value.upper()))
        cipher.stdin.flush()
        response = cipher.stdout.readline().rstrip()
        print(response)
        if command != "password" and response.startswith("RESULT "):
            history.append(response.split(" ", 1)[1])

    cipher.stdin.write("QUIT\n")
    cipher.stdin.flush()
    logger.stdin.write("QUIT\n")
    logger.stdin.flush()
    cipher.wait()
    logger.wait()
    return 0


if __name__ == "__main__":
    sys.exit(main())
