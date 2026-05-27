![Build 2026 Banner](img/banner-build-26.png)

# OD858 — Personalize Your Windows PC with AI: Build a Copilot Skill

Tell an AI assistant _"make everything pink!"_ and watch it transform your RGB lighting, desktop themes, and more. This session shows how to build a **GitHub Copilot Skill** that personalizes Windows using natural language — from Dynamic Lighting effects to full desktop theming.

> 📌 **This is a point-in-time snapshot.** The actively maintained version lives at:
> **[samanthamsong/windows-personalization-skill](https://github.com/samanthamsong/windows-personalization-skill)**
> Check there for the latest updates, bug fixes, and new features.

---

## 🏠 Getting Started (Own Environment)

Follow these steps after Build to set up the skill on your own machine.

### Prerequisites

| Requirement | Version | Install |
|---|---|---|
| Windows 11 | 22H2+ | — |
| Git | Any | `winget install Git.Git` |
| .NET SDK | 9.0+ | `winget install Microsoft.DotNet.SDK.9` |
| Python | 3.10+ | `winget install Python.Python.3.12` |
| WinAppCLI | 0.2+ | `winget install Microsoft.WinAppCli` |
| Developer Mode | — | Settings → System → For developers → ON |
| Dynamic Lighting device | — | Any [compatible](https://support.microsoft.com/en-us/windows/control-your-dynamic-lighting-devices-in-windows-8e9f9b1f-6844-4c5e-9873-d836e87fcb7f) RGB device |

### Quick Install

```powershell
# Install all prerequisites at once
winget install Git.Git Microsoft.DotNet.SDK.9 Python.Python.3.12 Microsoft.WinAppCli

# Clone the maintained repo as a Copilot skill
git clone https://github.com/samanthamsong/windows-personalization-skill.git "$HOME\.copilot\skills\windows-personalization"
cd "$HOME\.copilot\skills\windows-personalization"

# Run setup (first time: run as admin)
Start-Process powershell -Verb RunAs -ArgumentList "-File $PWD\setup.ps1"
```

> **Windows Settings (do both before running setup):**
> 1. **Developer Mode:** Settings → System → For developers → Developer Mode (ON)
> 2. **Dynamic Lighting:** Settings → Personalization → Dynamic Lighting → "Use Dynamic Lighting on my devices" (ON)

### Try It

```powershell
# Set your keyboard to a color
python modules/dynamic-lighting/lighting.py set-color "#FF6600"

# Run a per-lamp effect
python modules/dynamic-lighting/lighting.py run-effect koi-fish

# Or just tell Copilot what you want:
# "Make my keyboard breathe with purple"
# "Ocean waves on my keyboard"
```

---

## 🎯 Learning Outcomes

After this session, you will be able to:

- ✅ **Build a Copilot Skill** — create a SKILL.md and module structure that AI agents can discover and invoke automatically
- ✅ **Control Windows Dynamic Lighting** — use the LampArray API with .NET + Python to create per-lamp RGB keyboard effects
- ✅ **Create natural language interfaces** — connect human prompts ("make it pink!") to system-level Windows personalization APIs
- ✅ **Theme your entire desktop with AI** — orchestrate wallpaper, accent colors, and RGB lighting from a single prompt

---

## 💬 Keep Learning with Copilot (Suggested Prompts)

Paste these into GitHub Copilot Chat (with the [Microsoft Learn MCP Server](#-microsoft-learn-mcp-server) connected) to explore further:

1. **"How do I create a custom Copilot Skill that controls hardware APIs on Windows? Show me the SKILL.md format and how agents discover skills."**

2. **"Walk me through the Windows Dynamic Lighting API — how does a .NET app register for LampArray access, and how can Python scripts control individual lamp colors?"**

3. **"I want to build a theme engine that changes wallpaper, accent colors, and keyboard lighting from a single natural language prompt. What Windows APIs and patterns should I use?"**

---

## 🖥️ Technologies Used

| Technology | What it does |
|---|---|
| [Windows 11 Dynamic Lighting](https://learn.microsoft.com/windows/uwp/devices-sensors/lighting-dynamic-lamparray) | Per-lamp RGB control via LampArray API |
| [.NET 9](https://learn.microsoft.com/dotnet/core/whats-new/dotnet-9) | Driver for AppX package identity + LampArray access |
| [Python 3](https://www.python.org/) | Effect scripts, theme orchestration, CLI tools |
| [GitHub Copilot Skills](https://docs.github.com/en/copilot/building-copilot-skills) | SKILL.md-based agent extensibility |
| [WinAppCLI](https://github.com/nicola-brg/WinAppCLI) | AppX identity registration for dev scenarios |

---

## 📚 Resources and Next Steps

| Resource | Link |
|---|---|
| 🚀 **Build 2026 Next Steps** | [aka.ms/build26-next-steps](https://aka.ms/build26-next-steps) |
| 📦 **Maintained repo** (latest code) | [samanthamsong/windows-personalization-skill](https://github.com/samanthamsong/windows-personalization-skill) |
| 📖 Dynamic Lighting docs | [Windows Dynamic Lighting](https://learn.microsoft.com/windows/uwp/devices-sensors/lighting-dynamic-lamparray) |
| 📖 Copilot Skills docs | [Building Copilot Skills](https://docs.github.com/en/copilot/building-copilot-skills) |
| 📖 .NET 9 docs | [What's new in .NET 9](https://learn.microsoft.com/dotnet/core/whats-new/dotnet-9) |

---

## ⚙️ Microsoft Learn MCP Server

Connect Copilot to official Microsoft documentation for richer answers about the technologies in this session.

[![Install in VS Code](https://img.shields.io/badge/Install%20in%20VS%20Code-MCP%20Server-blue)](https://insiders.vscode.dev/redirect?url=vscode%3Amcp%2Finstall%3F%7B%22name%22%3A%22microsoft-learn%22%2C%22config%22%3A%7B%22type%22%3A%22sse%22%2C%22url%22%3A%22https%3A%2F%2Flearn.microsoft.com%2Fapi%2Fmcp%22%7D%7D)

The Microsoft Learn MCP Server is pre-configured in `.vscode/mcp.json` — it works automatically when you open this repo in VS Code or a Codespace.

---

## 👤 Content Owners

<!-- Add your GitHub handle, name, and avatar -->

| Role | Name | GitHub |
|---|---|---|
| Speaker | Samantha Song | [@samanthamsong](https://github.com/samanthamsong) |