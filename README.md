# AI Agent Workflows

Open-source plugins, skills, and reusable AI-agent workflows created and
maintained by me for ChatGPT, Codex, Claude, and other AI agents.

## Skills

| Skill | Purpose |
| --- | --- |
| [`app-idea-hunter`](skills/app-idea-hunter/) | Researches, validates, and scores app ideas using evidence from revenue, demand, distribution, and real user pain. |
| [`mobile-ui-pipeline-v2`](skills/mobile-ui-pipeline-v2/) | Designs and builds working Expo / React Native screens in one pass: short intake, parallel research fan-out, design direction, functional build, and self-review. Uses paid sources (e.g. Mobbin) when available, never requires them. |
| [`mvp-scoper`](skills/mvp-scoper/) | Cuts a validated idea to the smallest buildable v1: core loop, screen list, explicit not-in-v1 list, build plan, and a spec the build skill can consume. |
| [`landing-page-smoke-test`](skills/landing-page-smoke-test/) | Drafts a fake-door landing page, traffic plan, and a pre-registered pass/fail bar to test demand before building. Never publishes or posts. |
| [`monetization-designer`](skills/monetization-designer/) | Picks a pricing model and price points from competitor evidence, draws the free/paid line, and specs an honest paywall. |

Each skill follows the standard directory format: a required `SKILL.md` entry
point with optional `references/`, `scripts/`, and `assets/` resources beside it.

### Suggested flow

`app-idea-hunter` -> `landing-page-smoke-test` -> `mvp-scoper` ->
`monetization-designer` -> `mobile-ui-pipeline-v2`

## Install as a plugin (Claude Code)

```
/plugin marketplace add 889-dj/ai-agent-workflows
/plugin install ai-agent-workflows@ai-agent-workflows
```

Skills are then available as `/ai-agent-workflows:app-idea-hunter` and
`/ai-agent-workflows:mobile-ui-pipeline-v2` (and likewise for the other skills), and Claude also invokes them
automatically when a request matches their descriptions.

## Installation (any other agent)

Copy the skill directory into the skills location used by your agent, or point
your agent at the directory directly:

```bash
git clone https://github.com/889-dj/ai-agent-workflows.git
```

Consult your agent's documentation for its current skill-discovery location and
installation method.

## License

MIT
