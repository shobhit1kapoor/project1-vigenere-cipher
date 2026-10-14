#!/usr/bin/env python3
"""Interactive driver that coordinates the cipher and logger processes."""

import argparse
import os
import re
import subprocess
import sys


LETTERS_ONLY = re.compile(r"[A-Za-z]+\Z")


class ProjectSession:
    def __init__(self, log_path):
        project_dir = os.path.dirname(os.path.abspath(__file__))
        logger_path = os.path.join(project_dir, "logger.py")
        encryptor_path = os.path.join(project_dir, "encryptor.py")
        python = sys.executable

        self.history = []
        self.logger = None
        self.encryptor = None
        self.logger_warning_shown = False

        try:
            self.logger = subprocess.Popen(
                [python, logger_path, log_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                bufsize=1,
            )
            self.encryptor = subprocess.Popen(
                [python, encryptor_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                bufsize=1,
            )
        except OSError:
            self.shutdown()
            raise

        self.log("START", "Driver started")

    def log(self, action, message):
        """Send one protocol line to the logger process."""
        if self.logger is None:
            return
        if self.logger.poll() is not None:
            if not self.logger_warning_shown:
                print("Warning: the logger process stopped unexpectedly.", file=sys.stderr)
                self.logger_warning_shown = True
            return
        if self.logger.stdin is None:
            return

        safe_message = str(message).replace("\r", " ").replace("\n", " ")
        try:
            self.logger.stdin.write("{} {}\n".format(action, safe_message))
            self.logger.stdin.flush()
        except (BrokenPipeError, OSError):
            print("Warning: the logger process stopped unexpectedly.", file=sys.stderr)

    def request_cipher(self, command, argument=None):
        """Send one command to the cipher and read its one-line response."""
        if self.encryptor is None or self.encryptor.poll() is not None:
            return "ERROR Encryption process stopped unexpectedly"
        if self.encryptor.stdin is None or self.encryptor.stdout is None:
            return "ERROR Encryption process streams are unavailable"

        line = command if argument is None else "{} {}".format(command, argument)
        try:
            self.encryptor.stdin.write(line + "\n")
            self.encryptor.stdin.flush()
            response = self.encryptor.stdout.readline()
        except (BrokenPipeError, OSError):
            return "ERROR Could not communicate with encryption process"

        if not response:
            return "ERROR Encryption process stopped unexpectedly"
        return response.rstrip("\r\n")

    def show_history(self):
        if not self.history:
            print("History is empty.")
            return

        print("History:")
        for index, value in enumerate(self.history, start=1):
            print("  {}. {}".format(index, value))

    def prompt_for_new_string(self, purpose):
        try:
            return input("Enter {}: ".format(purpose))
        except EOFError:
            print()
            return None

    def choose_string(self, purpose):
        """Choose a new value or a history item; None means cancel."""
        while True:
            try:
                choice = input(
                    "Use [n]ew {}, [h]istory, or [q]uit this command? ".format(purpose)
                ).strip().lower()
            except EOFError:
                print()
                return None

            if choice in ("q", "quit", "cancel"):
                return None
            if choice in ("n", "new"):
                return self.prompt_for_new_string(purpose), True
            if choice not in ("h", "history"):
                print("Choose n, h, or q.")
                continue

            self.show_history()
            while True:
                try:
                    selection = input(
                        "Select a number, [n]ew {}, or [q]uit this command: ".format(purpose)
                    ).strip().lower()
                except EOFError:
                    print()
                    return None

                if selection in ("q", "quit", "cancel"):
                    return None
                if selection in ("n", "new"):
                    return self.prompt_for_new_string(purpose), True
                if not selection.isdigit():
                    print("Enter a history number, n, or q.")
                    continue

                index = int(selection)
                if 1 <= index <= len(self.history):
                    return self.history[index - 1], False
                print("That history number is not available.")

    @staticmethod
    def valid_letters(value):
        return bool(value and LETTERS_ONLY.fullmatch(value))

    @staticmethod
    def response_parts(response):
        kind, separator, message = response.partition(" ")
        return kind, message if separator else ""

    def handle_password(self):
        self.log("COMMAND", "password")
        chosen = self.choose_string("password")
        if chosen is None:
            self.log("RESULT", "password command cancelled")
            return

        value, _is_new = chosen
        if value is None:
            self.log("RESULT", "password command cancelled at input")
            return
        if not self.valid_letters(value):
            print("Error: password must contain only letters.")
            self.log("ERROR", "password rejected; passkey was not logged")
            return

        response = self.request_cipher("PASS", value.upper())
        kind, message = self.response_parts(response)
        if kind == "RESULT":
            print("Password set.")
            self.log("RESULT", "password set")
        else:
            print("Error: {}".format(message or "password was not accepted"))
            self.log("ERROR", "password command failed")

    def handle_cipher_action(self, action):
        self.log("COMMAND", action)
        chosen = self.choose_string("string to {}".format(action))
        if chosen is None:
            self.log("RESULT", "{} command cancelled".format(action))
            return

        value, is_new = chosen
        if value is None:
            self.log("RESULT", "{} command cancelled at input".format(action))
            return

        # Keep each nonempty newly entered string in this run's history, even
        # when validation rejects it, as the assignment asks to retain inputs.
        if is_new and value:
            self.history.append(value)

        if not self.valid_letters(value):
            print("Error: input must contain only letters.")
            self.log("ERROR", "{} rejected; input must contain only letters".format(action))
            return

        response = self.request_cipher(action.upper(), value.upper())
        kind, message = self.response_parts(response)
        if kind == "RESULT":
            print("Result: {}".format(message))
            if message:
                self.history.append(message)
            self.log("RESULT", "{} {}".format(action, message or "completed"))
        else:
            print("Error: {}".format(message or "operation failed"))
            self.log("ERROR", "{} {}".format(action, message or "operation failed"))

    def run(self):
        print("Project 1: process and pipe demonstration")
        print("Commands: password, encrypt, decrypt, history, quit")

        while True:
            try:
                command = input("command> ").strip().lower()
            except EOFError:
                print()
                self.log("COMMAND", "end of input")
                break

            if not command:
                continue

            if command == "password":
                self.handle_password()
            elif command == "encrypt":
                self.handle_cipher_action("encrypt")
            elif command == "decrypt":
                self.handle_cipher_action("decrypt")
            elif command == "history":
                self.log("COMMAND", "history")
                self.show_history()
                self.log("RESULT", "history displayed ({} entries)".format(len(self.history)))
            elif command == "quit":
                self.log("COMMAND", "quit")
                self.log("RESULT", "driver shutting down")
                break
            else:
                self.log("COMMAND", "unknown command")
                self.log("ERROR", "unknown command")
                print("Unknown command. Choose password, encrypt, decrypt, history, or quit.")

        self.log("EXIT", "Driver exited")
        print("Goodbye.")

    def shutdown(self):
        """Tell both child processes to stop, then reap them."""
        if self.encryptor is not None:
            try:
                if self.encryptor.poll() is None and self.encryptor.stdin is not None:
                    self.encryptor.stdin.write("QUIT\n")
                    self.encryptor.stdin.flush()
                    self.encryptor.stdin.close()
                self.encryptor.wait(timeout=3)
            except (BrokenPipeError, OSError, subprocess.TimeoutExpired):
                self.encryptor.terminate()
                self.encryptor.wait()
            finally:
                if self.encryptor.stdout is not None:
                    self.encryptor.stdout.close()

        if self.logger is not None:
            try:
                if self.logger.poll() is None and self.logger.stdin is not None:
                    self.logger.stdin.write("QUIT\n")
                    self.logger.stdin.flush()
                    self.logger.stdin.close()
                self.logger.wait(timeout=3)
            except (BrokenPipeError, OSError, subprocess.TimeoutExpired):
                self.logger.terminate()
                self.logger.wait()
            finally:
                if self.logger.stdout is not None:
                    self.logger.stdout.close()


def main():
    parser = argparse.ArgumentParser(description="Run the Project 1 driver")
    parser.add_argument("log_file", help="path for the activity log")
    args = parser.parse_args()

    session = None
    try:
        session = ProjectSession(args.log_file)
        session.run()
        return 0
    except (OSError, RuntimeError) as error:
        print("Could not start the project: {}".format(error), file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nInterrupted.")
        if session is not None:
            session.log("EXIT", "Driver interrupted")
        return 130
    finally:
        if session is not None:
            session.shutdown()


if __name__ == "__main__":
    sys.exit(main())
