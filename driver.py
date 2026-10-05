#!/usr/bin/env python3
"""First driver draft: start the children and pass simple commands."""
import os
import subprocess
import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: python driver.py LOG_FILE")
        return 2

    folder = os.path.dirname(os.path.abspath(__file__))
    logger = subprocess.Popen(
        [sys.executable, os.path.join(folder, "logger.py"), sys.argv[1]],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, encoding="utf-8", bufsize=1
    )
    cipher = subprocess.Popen(
        [sys.executable, os.path.join(folder, "encryptor.py")],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, encoding="utf-8", bufsize=1
    )

    print("Commands: password, encrypt, decrypt, quit")
    while True:
        try:
            command = input("command> ").strip().lower()
        except EOFError:
            command = "quit"
        if command == "quit":
            break
        if command == "password":
            value = input("New password: ")
            cipher.stdin.write("PASS {}\n".format(value.upper()))
            cipher.stdin.flush()
            print(cipher.stdout.readline().rstrip())
        elif command in ("encrypt", "decrypt"):
            value = input("String: ")
            cipher.stdin.write("{} {}\n".format(command.upper(), value.upper()))
            cipher.stdin.flush()
            print(cipher.stdout.readline().rstrip())
        else:
            print("Unknown command.")

    cipher.stdin.write("QUIT\n")
    cipher.stdin.flush()
    logger.stdin.write("QUIT\n")
    logger.stdin.flush()
    cipher.wait()
    logger.wait()
    return 0


if __name__ == "__main__":
    sys.exit(main())
