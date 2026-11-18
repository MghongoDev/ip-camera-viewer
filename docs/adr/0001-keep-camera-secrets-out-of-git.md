# 0001 Keep the camera address out of Git

Status: Accepted

## Context

The camera URL can carry a password. A commit makes that value public and permanent in the repository history. Deleting a file in a later commit does not remove it from history.

## Decision

Store the real address in `.env`, which `.gitignore` excludes. Commit `.env.example` with placeholders only. Read values through `config.py`. Print a masked form in all console output and logs.

## Consequences

A new user copies `.env.example` to `.env` before the first run. A secrets audit checks tracked files and history before each push. The implementation guide stays untracked so its sample values never enter the repository.
