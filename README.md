# Project 1: Process-Based Vigenere Cipher

**Author:** Shobhit Kapoor

This program encrypts and decrypts alphabetic strings with a repeating-key Vigenere cipher. The interactive driver starts two child processes: one handles cipher commands, and the other writes activity records. The processes communicate through standard-input and standard-output pipes. The project uses only the Python standard library.

## Files

- `driver.py` — interactive menu, input checks, child-process management, and current-run history.
- `encryptor.py` — line-based `PASS`, `ENCRYPT`, `DECRYPT`, and `QUIT` command handler.
- `logger.py` — appends timestamped action and result records to the selected log file.
- `devlog.md` — dated work-session notes and project corrections.
- `.gitignore` — excludes Python cache files and generated `.log` files.

## Requirements

Python 3.7 or newer. No packages need to be installed.

## Run

From this directory, start the driver and choose a path for the activity log:

**Windows**

```powershell
py -3 .\driver.py activity.log
```

**Linux or macOS**

```sh
python3 driver.py activity.log
```

The log is created if it does not exist. Later runs append to the same file. A relative path such as `activity.log` is resolved from the directory where the command is run.

## Commands

At the `command>` prompt, enter one of these commands:

- `password` — set the key. The key must contain only letters.
- `encrypt` — encrypt a new string or a string from history.
- `decrypt` — decrypt a new string or a string from history.
- `history` — list cipher inputs and successful results entered during this run.
- `quit` — stop the driver and both child processes.

For a password, encryption input, or decryption input, choose `n` to enter a new value, `h` to select from history where available, or `q` to cancel the command. Inputs are case-insensitive and may contain ASCII letters only. The driver stores each newly entered cipher input in history even when it is rejected, and adds successful results. Passwords are excluded from both history and the activity log. History is kept in memory for the current run and is cleared when the program exits.

The cipher process returns a `RESULT` or `ERROR` line for each command. For example, key `LEMON` encrypts `ATTACKATDAWN` to `LXFOPVEFRNHR`.

The logger writes records in this format, using the computer's local time:

```text
YYYY-MM-DD HH:MM [ACTION] MESSAGE
```

The driver logs commands and outcomes without writing password values. The repository includes its Git history; the course archive should include the `.git` directory as specified in the project instructions.
