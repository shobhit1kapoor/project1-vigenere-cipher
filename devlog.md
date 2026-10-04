> **Reference example only:** the author name Jonathan, dates, session notes, and commit timeline in this copy are fictional teaching material. They are not a factual record of anyone's work and should not be presented as one. The code is included so you can compare a finished project structure with your own.

# Development Log

## 2026-09-30 6:05 PM — Session start: Repository and process boundaries

**Thoughts and plan:**

I read the project description and separated the work into the driver, encryption process, and logger. I chose Python because the course permits `subprocess`, and its standard library is enough for the required processes and pipes.

Plan: create the repository and devlog first, then define the messages each child process will accept. I want the driver to own the interactive menu while the children each have one focused responsibility.

## 2026-09-30 7:45 PM — Session reflection: Repository and process boundaries

**Progress and next step:**

The repository now has a short map of the three programs and the initial command-line shape. I have not implemented the children yet. The main design decision is to use one line per request so each response can be read without ambiguity.

Next session: make the logger accept a file path and append timestamped action/message lines until `QUIT`.

## 2026-10-02 6:05 PM — Session start: Logger process

**Thoughts and plan:**

Since the last session I settled the logging protocol: the first token is an action, followed by the message. The driver should not open the log directly; it should send records to the logger over the logger's standard input.

Plan: implement append mode, local 24-hour timestamps, and a clean `QUIT` path. I will flush each record so it is written during the run.

## 2026-10-02 7:45 PM — Session reflection: Logger process

**Progress and next step:**

The logger now opens the requested path in append mode, formats each message as `YYYY-MM-DD HH:MM [ACTION] MESSAGE`, and exits on `QUIT`. I kept file handling in that process so the driver remains a client of the logging protocol.

Next session: implement the cipher process and its remembered key.

## 2026-10-04 6:05 PM — Session start: Vigenere command process

**Thoughts and plan:**

The logger protocol is straightforward. The cipher process needs to keep a key between commands, and it should report an error if encryption or decryption happens before `PASS`. The assignment's example gives a useful known answer for checking the implementation.

Plan: add `PASS`, `ENCRYPT`, `DECRYPT`, and `QUIT`, with one `RESULT` or `ERROR` line per request.

## 2026-10-04 7:45 PM — Session reflection: Vigenere command process

**Progress and next step:**

The cipher process now maintains its passkey and transforms A-Z text with a repeating Vigenere key. It normalizes case and rejects inputs outside letters. The passkey is not echoed in the response.

Next session: connect the driver to the two children and verify the line-oriented shape during integration.
