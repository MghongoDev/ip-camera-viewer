# 0009 Use the Divio four-part documentation layout

Status: Accepted

## Context

One long README cannot answer four different questions well. A newcomer, an operator, a developer and a reviewer each need a different entry point.

## Decision

Keep README as the entry point and split the rest into `docs/tutorials/`, `docs/how-to/`, `docs/reference/` and `docs/explanation/`. Add `GLOSSARY.md` and `docs/adr/`. Apply the prose rules to every document.

## Consequences

A reader finds the right document in seconds. Tutorials never mix with reference material. Each document states its prerequisites and its failure path.
