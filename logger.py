#!/usr/bin/env python3
"""Append timestamped messages received from the driver to a log file."""

import sys
from datetime import datetime


def run(log_path):
    try:
        with open(log_path, "a", encoding="utf-8") as log_file:
            for raw_line in sys.stdin:
                line = raw_line.rstrip("\r\n")
                if line == "QUIT":
                    break
                if not line:
                    continue

                action, separator, message = line.partition(" ")
                timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M")
                if separator:
                    log_file.write("{} [{}] {}\n".format(timestamp, action, message))
                else:
                    log_file.write("{} [{}]\n".format(timestamp, action))
                log_file.flush()
    except OSError as error:
        print("Logger could not write '{}': {}".format(log_path, error), file=sys.stderr)
        return 1

    return 0


def main():
    if len(sys.argv) != 2:
        print("Usage: python logger.py LOG_FILE", file=sys.stderr)
        return 2
    return run(sys.argv[1])


if __name__ == "__main__":
    sys.exit(main())
