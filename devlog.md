> **Reference example only:** the author name Jonathan, dates, session notes, and commit timeline in this copy are fictional teaching material. They are not a factual record of anyone's work and should not be presented as one. The code is included so you can compare a finished project structure with your own.

# Development Log

## 2026-09-30 6:05 PM — Session start: Repository and process boundaries

**Thoughts and plan:**

I read the project description and separated the work into the driver, encryption process, and logger. I chose Python because the course permits `subprocess`, and its standard library is enough for the required processes and pipes.

Plan: create the repository and devlog first, then define the messages each child process will accept. I want the driver to own the interactive menu while the children each have one focused responsibility.
