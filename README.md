# Project 1: Vigenere Cipher

**Author:** Shobhit Kapoor

This project has three Python programs. `driver.py` handles the menu and starts `encryptor.py` and `logger.py` as child processes. The driver sends commands to them through standard input and reads their responses through standard output. The project uses Python's standard library only.

## Files

- `driver.py` — menu, input checks, process communication, and history for the current run.
- `encryptor.py` — handles `PASS`, `ENCRYPT`, `DECRYPT`, and `QUIT` commands and performs the Vigenere cipher.
- `logger.py` — appends timestamped activity records to the log file.
- `devlog.md` — development notes and corrections.
- `.gitignore` — excludes Python cache files and generated log files.

## Run

Python 3.7 or newer is required. No packages need to be installed. Run the driver from this directory and give it a log file path:

**Windows**

```powershell
py -3 .\driver.py activity.log
```

**Linux or macOS**

```sh
python3 driver.py activity.log
```

The logger creates the file if needed and appends to it on later runs. Relative paths are resolved from the directory where the command is run.

## Using the program

At `command>`, enter `password`, `encrypt`, `decrypt`, `history`, or `quit`. For a password or cipher input, choose `n` to enter a new value, `h` to select one from history, or `q` to cancel. Inputs can use upper- or lowercase ASCII letters only.

History lasts until the program exits. Each new encryption or decryption input is saved, including an input rejected by validation. Successful results are saved too. Passwords are not added to history and their values are not written to the activity log.

For example, with key `LEMON`, encrypting `ATTACKATDAWN` gives `LXFOPVEFRNHR`.

## Activity log

The logger uses the computer's local time and writes one record per line:

```text
YYYY-MM-DD HH:MM [ACTION] MESSAGE
```

The repository includes its Git history. The exact times for the first 27 commits were not saved; with my instructor's approval, I estimated them from memory. They use Chicago local time (UTC−05:00). Later review commits use the times when that work was done. The development log records this history and its limits. Codex assisted with the review and fixes recorded in the development log.

Include the `.git` directory when creating the course submission ZIP so the commit history is available.
