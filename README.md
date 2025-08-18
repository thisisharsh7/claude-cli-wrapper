
# ccui — Claude Code UI Generator (Frontend-only)

A minimal CLI that wraps Claude Code to generate landing pages from a reference URL + product description.  
**Scope:** frontend only (HTML/Tailwind or React), with UI/UX heuristics baked into the prompt.

## ✨ What it does
1. Opens a URL with Playwright
2. Captures a full-page screenshot and DOM snapshot
3. Builds a high-quality prompt automatically
4. Calls your Claude Code CLI (no extra model costs)
5. Saves generated code to `output/landing-page/`
6. (Optional) Previews locally

## 🧰 Prerequisites
- Python 3.9+
- Claude Code CLI installed and working (e.g., a `claude` command)
- macOS/Linux/WSL is fine
- Chrome is *not* required (uses Playwright Chromium)

## 🚀 Step-by-step Setup

```bash
# 1) Create & activate a virtualenv
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# 2) Install this package (editable) + dependencies
pip install -e .

# 3) Install Playwright browsers
ccui init

# 4) Generate a landing page inspired by a URL
ccui gen --url https://linear.app --desc "AI bug tracker for teams"

# 5) Preview locally (pick one)
python -m http.server -d output/landing-page 3000
# or if you have node:
# npx serve output/landing-page -p 3000
```

## 🧪 Example
```bash
ccui gen --url https://stripe.com --desc "Crypto payroll platform for startups"
```

## ⚙️ Commands
- `ccui init` — installs Playwright browsers
- `ccui gen --url <URL> --desc "<product description>" [--framework html|react] [--theme minimal|brutalist|playful] [--sections hero,features,pricing,footer] [--claude-cmd claude]`

## 📝 Configure (optional)
You can create a `ccui.yaml` in the current directory:

```yaml
framework: html    # html or react
theme: minimal
sections: [hero, features, pricing, footer]
claude_cmd: claude
output_dir: output/landing-page
```

CLI flags always override config values.

## 🆘 Troubleshooting
- If `ccui gen` fails, check:
  - Is your `claude` CLI installed and accessible on PATH?
  - Does the URL load without consent gates / blockers?
  - Try `--framework html` (simpler than React)


