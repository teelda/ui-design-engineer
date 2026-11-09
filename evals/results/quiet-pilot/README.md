# Quiet-task pilot — 2026-11-09

This is one exploratory pair, **not evidence that the skill improves design quality**. The fixture and scoring rules were created by the same maintainer who revised the skill, and the run was not blindly scored. The artifacts are included so the result is inspectable.

| Condition | Agent | Prompt difference | Outcome |
|---|---|---|---|
| Control | Codex CLI 0.160.0, `gpt-6.1-sol`, one run | No skill path | Enlarged Review link targets to 44×44px and added request-specific accessible names. |
| With skill | Same CLI and model, one run | Explicitly read `skills/ui-design-engineer/SKILL.md` | Enlarged Review link targets to 44px tall and added the same accessible names. |

Both runs used fresh copies of the [quiet task](../../fixtures/quiet-task/README.md), the same task wording, isolated CLI sessions, and the same workspace-write sandbox. Both preserved visible content and destination URLs. Neither made broad decorative changes. The control added a 44px minimum width; the skill run did not. The visible difference is too small to infer a skill benefit.

Both agents reported that Chrome could not launch in their sandbox, so neither verified 390px/desktop rendering. This pilot has no screenshots, blind visual score, interaction score, or repeated runs. The raw final files and agent replies are saved beside this note. A proper comparison still needs repeated pairs on unfamiliar tasks and independent scoring.
