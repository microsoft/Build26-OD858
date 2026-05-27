# AGENTS.md — Security Rules and Repo Guidelines for AI Agents

## Security Rules

- **Do not commit secrets** (API keys, tokens, passwords) into source code.
- **Do not share sensitive data** with third-party systems.
- **Do not modify** `.github/`, `.vscode/`, or `AGENTS.md` files unless explicitly asked.
- **Do not delete** files in `img/` — the banner image is used by the README.

## Repo Guidelines

- This is a **Build 2026 session repository** for session **OD858**.
- The `src/` directory contains a point-in-time snapshot of the [Windows Personalization Skill](https://github.com/samanthamsong/windows-personalization-skill).
- The actively maintained code lives at the link above — direct attendees there for the latest updates.
- The `_remove-before-publish/` directory contains internal-only materials and is `.gitignored`.
- All attendee-facing content should be in the repo root, `src/`, `docs/`, or `img/`.

## Content Standards

- Content must be audience-first: help the developer who attended the session.
- No vaporware — only reference real, available products and experiences.
- Include clear takeaways attendees can act on immediately.
- All suggested Copilot prompts should work with the Microsoft Learn MCP Server connected.
