# Git Setup Guide v2

Your local repository is initialized and ready! Here's how to connect it to a remote repository.

## Option 1: GitHub

### Create a new GitHub repository:
1. Go to [github.com/new](https://github.com/new)
2. Name it: `techrob-action360-agent`
3. **Don't** initialize with README (you have one already)
4. Click "Create repository"

### Connect your local repo:
```bash
cd c:\src\techrob_action360_agent
git remote add origin https://github.com/YOUR_USERNAME/techrob-action360-agent.git
git branch -M main
git push -u origin main
```

---

## Option 2: Azure Repos (Recommended for Microsoft Azure integration)

### Create a new Azure DevOps project:
1. Go to [dev.azure.com](https://dev.azure.com)
2. Create new project: `TechRob`
3. Navigate to **Repos**
4. Select **Import a repository**
5. Source Type: **Git**
6. Clone URL: Use your local repo URL or initialize from scratch

### Or push existing local repo:
```bash
cd c:\src\techrob_action360_agent
git remote add origin https://dev.azure.com/YOUR_ORG/TechRob/_git/techrob-action360-agent
git branch -M main
git push -u origin main
```

---

## Option 3: GitLab

Similar to GitHub, but use GitLab URL:
```bash
git remote add origin https://gitlab.com/YOUR_USERNAME/techrob-action360-agent.git
git push -u origin main
```

---

## Common Git Commands

### Check current status:
```bash
git status
```

### View commit history:
```bash
git log --oneline
```

### View configured remotes:
```bash
git remote -v
```

### Create a feature branch:
```bash
git checkout -b feat/mcp-integration
# Make changes
git add .
git commit -m "feat: Add MCP server integration"
git push -u origin feat/mcp-integration
```

### Pull latest changes:
```bash
git pull origin main
```

---

## Branching Strategy

Follow conventional commits and these branch patterns:

- `main` - Production-ready code
- `feat/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code improvements

Example:
```bash
git checkout -b feat/add-streaming-response
# ... make changes ...
git push -u origin feat/add-streaming-response
```

Then create a pull request on your hosting platform.

---

## Current Commit History

```
2ae6d5b docs: Add LICENSE and update project guidelines with git strategy
6322366 Initial commit: TechRob Action360 Agent with Foundry GPT-4o integration
```

---

## Next: Set Your Git Identity (if not already done)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

View current config:
```bash
git config --list
```
