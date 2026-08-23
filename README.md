# AI Agent Workflows

Open-source plugins, skills, and reusable AI-agent workflows created and
maintained by me for ChatGPT, Codex, Claude, and other AI agents.

## Skills

| Skill | Purpose |
| --- | --- |
| [`app-idea-hunter`](skills/app-idea-hunter/) | Researches, validates, and scores app ideas using evidence from revenue, demand, distribution, and real user pain. |

Each skill follows the standard directory format: a required `SKILL.md` entry
point with optional `references/`, `scripts/`, and `assets/` resources beside it.

## Installation

Copy the skill directory into the skills location used by your agent, or point
your agent at the directory directly:

```bash
git clone https://github.com/889-dj/ai-agent-workflows.git
```

Consult your agent's documentation for its current skill-discovery location and
installation method.


## Credits

The app-idea-hunter skill's harvest methodology (Phase 1) draws on the idea-sourcing approaches from:

- Steven Cravotta — "How I Find App Ideas That Print"
- Simon Grimm — short on app-idea market analysis
- Builders Central — "This is How I Find App Ideas That Print"

## License

MIT
