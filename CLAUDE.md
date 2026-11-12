# Little WOW Lab media repo

Public hosting for Little WOW Lab social media images and videos, plus the weekly content system.

- Read BRAND.md (facts and hard rules), CREATIVE.md (the quality bar) and PLAYBOOK.md (weekly run) before any content work.
- Agents live in .claude/agents: scout, analyst, strategist, creator, reviewer, publisher.
- Render media: `python3 tools/render.py content/<week>/plan.json` (needs playwright + ffmpeg).
- Everything in this repo is public. Never commit the workbook PDF, templates, credentials, or the owner's personal data.
- Nothing is published without the owner's explicit approval of that week's batch.
