# Activation Audits

Activation audits record whether a repository has crossed from _described_ to
_shipped_. Unlike the [security audits](../README.md) in the parent directory,
these audits answer a single question:

> Can a consumer actually **run** something here - via a live URL, an
> installable package, a runnable release, or a documented execution path?

## Verdicts

| Verdict    | Meaning                                                       |
| ---------- | ------------------------------------------------------------- |
| `activate` | Shipping evidence exists; promote / surface the repository.   |
| `park`     | No shipping surface, but the repo is functioning as intended. |
| `retire`   | No shipping surface and no remaining role; decommission.      |

## Naming Convention

One file per audit, named `YYYY-MM-DD-EV-<issue>.md`, where the date is the
audit event date and `<issue>` is the tracking issue number.

## Records

| Date       | Repository                                            | Verdict    | Issue                                                           |
| ---------- | ----------------------------------------------------- | ---------- | --------------------------------------------------------------- |
| 2026-06-11 | [`organvm-i-theoria/.github`](./2026-06-11-EV-447.md) | `activate` | [#447](https://github.com/organvm-i-theoria/.github/issues/447) |
