# Moving this project's knowledge to another Claude account

Claude doesn't carry memory between accounts or chats, so moving the project means giving the other account the right files. Everything it needs is in this repo:

| File | What it gives the other account |
|---|---|
| `.claude/skills/pnw-trenchless-project/` | Client facts, approved design, your feedback history, hard rules |
| `.claude/skills/bricks-acss-build-conventions/` | How you build in Bricks + ACSS + Fluent Forms + HappyFiles |
| `CLAUDE.md` | Auto-loaded by Claude Code in this repo; points to everything else |
| `pnw-trenchless/index.html` + `assets/` | The approved design itself |
| `pnw-trenchless/BRICKS-HANDOFF.md`, `BUILD-CONVENTIONS.md`, `screenshots/` | Build details and visuals |
| `pnw-trenchless/transfer/*.zip` | The two skills packaged for upload |

## Option A: the other account uses claude.ai (web, desktop or mobile)

1. **Upload the two skills.** In claude.ai open **Settings → Capabilities**, make sure Skills are on, then upload:
   - `pnw-trenchless/transfer/pnw-trenchless-project.zip`
   - `pnw-trenchless/transfer/bricks-acss-build-conventions.zip`
   (If your organization manages skills centrally, an admin can add them for everyone instead.)
2. **Create a Project** called "PNW Trenchless" and add these files to its project knowledge:
   - `pnw-trenchless/BRICKS-HANDOFF.md`
   - `pnw-trenchless/BUILD-CONVENTIONS.md`
   - `pnw-trenchless/index.html`
   - a few images from `pnw-trenchless/screenshots/`
3. **Project instructions:** paste the "Hard rules" section from `CLAUDE.md`.
4. **Connectors:** in **Settings → Connectors**, add and sign in to the WordPress (Novamira) connector for the PNW site once you've chosen it, plus GitHub if that account should push to this repo.

## Option B: the other account uses Claude Code (terminal, IDE or claude.ai/code)

1. Give that account access to this GitHub repo (`shibupandit/hello-world`) and the working branch.
2. Open the repo. `CLAUDE.md` loads automatically, and the skills in `.claude/skills/` are picked up for this project.
3. To use the Bricks conventions skill in **every** project on that machine, copy it to the user skills folder:
   ```
   mkdir -p ~/.claude/skills
   cp -r .claude/skills/bricks-acss-build-conventions ~/.claude/skills/
   ```
4. Connect the Novamira WordPress connector for the chosen PNW site (claude.ai connector settings, or the MCP config in Claude Code).

## First message to send on the other account

> Read CLAUDE.md and the pnw-trenchless-project and bricks-acss-build-conventions skills, then summarize where the PNW Trenchless project stands and what's still unknown. Don't change anything yet.

If the summary matches the "Design decisions" and "Still unknown" sections of the project skill, the transfer worked.

## Keeping both accounts in sync

When a decision changes (the WordPress site is chosen, Mike sends reviews, the design changes), update `.claude/skills/pnw-trenchless-project/SKILL.md`, commit, and re-upload the zip on claude.ai. The repo copy stays the single source of truth.
