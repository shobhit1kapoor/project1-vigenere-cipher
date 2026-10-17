# Project 1 reference model: process-based Vigenere cipher

> **Reference example only:** the author name Jonathan, dates, session notes, and commit
> timeline in this copy are fictional teaching material. They are not a factual record of
> anyone's work and should not be presented as one. The code is included so you can compare
> a finished project structure with your own.

This project has three Python programs. Run `driver.py`; it starts the encryption and
logger programs as child processes and communicates with them through standard-input and
standard-output pipes. It uses only the Python standard library.

## Files

- `driver.py` — interactive menu, subprocess launcher, input validation, and per-run history.
- `encryptor.py` — line-oriented `PASS`, `ENCRYPT`, `DECRYPT`, and `QUIT` protocol with a
  repeating-key Vigenere cipher.
- `logger.py` — reads action/message lines and appends timestamped records until `QUIT`.
- `devlog.md` — two timestamped entries for each illustrative work session.
- `.gitignore` — omits Python cache files and generated log files from Git.

## Run

On Linux or macOS:

```sh
python3 driver.py activity.log
```

On Windows:

```powershell
py -3 .\driver.py activity.log
```

No package installation or IDE is required. The log file is created if needed and appended
to on later runs.

## Commands and behavior

- `password` — set the current key from a new letters-only value or a history item.
- `encrypt` and `decrypt` — process a new string or a history item.
- `history` — display strings entered for encryption/decryption and successful results in
  the current run.
- `quit` — send `QUIT` to the child processes and exit.

The history menu accepts an item number, `n` for a new value, or `q` to cancel. Inputs are
case-insensitive and must contain only ASCII letters. New passwords are never stored in
history or written to the log. Cipher inputs and successful results are kept in memory only
for the current run.

Logger records use `YYYY-MM-DD HH:MM [ACTION] MESSAGE` with the machine's local time. The
cipher process responds with `RESULT` or `ERROR` lines.

## Reading the illustrative history

The commits are dated every other day from September 30 through October 16, 2026. Each
session has an opening plan, an implementation commit, and a closing reflection. This is a
model of how to organize real work; the dates and author are fictional. A real project log
should record the student's actual decisions and progress. Review the implementation and
perform manual checks before relying on it.

## Packaging a real course project

For an actual submission, follow the course instructions: review the project, make sure the
working tree is clean, include a README and devlog, and ZIP the whole Git repository,
including `.git`.


This reference copy's `Jonathan` author and every-other-day commit dates are simulated. They illustrate a process record and must not be mistaken for actual activity.
