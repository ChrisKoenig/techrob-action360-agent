# Git Setup Guide

Your local repository is initialized and ready for collaboration. This guide covers setup, workflow, and best practices.

## Repository Status

- **Remote**: Already configured at https://github.com/ChrisKoenig/techrob-action360-agent
- **Main Branch**: Production-ready code with MCP integration and routing
- **Current Phase**: Phase 2 complete (MCP + Routing), Phase 3 planning (Multi-platform deployment)

## Connecting to GitHub

If you're setting up on a new machine:

### 1. Clone the repository:
```bash
git clone https://github.com/ChrisKoenig/techrob-action360-agent.git
cd techrob-action360-agent
```

### 2. Set your identity (if needed):
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 3. Verify remote:
```bash
git remote -v
# Should show:
# origin  https://github.com/ChrisKoenig/techrob-action360-agent.git (fetch)
# origin  https://github.com/ChrisKoenig/techrob-action360-agent.git (push)
```

---

## Development Workflow

### 1. Start Feature Development

```bash
# Create feature branch
git checkout -b feat/your-feature-name

# Example branches:
git checkout -b feat/add-teams-integration
git checkout -b fix/mcp-null-issue
git checkout -b docs/update-readme
```

### 2. Make Changes

```bash
# Check status
git status

# Stage changes
git add src/agent.py config/instructions_routing.md

# Or stage all
git add .
```

### 3. Commit with Conventional Commits

Follow this format: `<type>: <description>`

**Types**:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation updates
- `refactor:` - Code improvements
- `test:` - Test additions
- `chore:` - Build, dependencies, etc.

**Examples**:
```bash
git commit -m "feat: Add routing analysis with 7-phase engine"
git commit -m "fix: Resolve MCP tool project name issue"
git commit -m "docs: Update README with current API endpoints"
git commit -m "refactor: Simplify instruction loading logic"
```

### 4. Push and Create Pull Request

```bash
git push -u origin feat/your-feature-name
```

Then create a PR on GitHub:
1. Go to https://github.com/ChrisKoenig/techrob-action360-agent
2. Click "Pull Requests"
3. Click "New Pull Request"
4. Select your branch
5. Add description and submit

---

## Branching Strategy

```
main (production-ready)
├── feat/add-teams-integration (feature branch)
├── feat/phase3-deployment (feature branch)
├── fix/api-streaming-bug (fix branch)
└── docs/update-guides (documentation branch)
```

**Branch Rules**:
- `main` - Always production-ready, fully tested
- Feature/fix branches - Created from main, target main in PR
- Delete branch after PR merge

### Current Work

The project uses feature branches for development:

**Active Branches**:
- `multi-instructions` - Dynamic instruction sets (merged to main)
- `feat/*` - New features for Phase 3

**Recent Merges**:
- PR #2 "added routing" - Dynamic instructions with routing engine

---

## Common Git Commands

### Check Status
```bash
git status                 # See what changed
git log --oneline          # View commit history
git branch -a              # List all branches
git remote -v              # View remote configuration
```

### Update from Main
```bash
# If on your feature branch
git fetch origin            # Fetch latest
git rebase origin/main      # Apply main's changes
# If conflicts exist, resolve them, then:
git add .
git rebase --continue
```

### Undo Changes
```bash
git checkout -- src/file.py          # Undo changes to file
git reset HEAD src/file.py           # Unstage file
git reset --hard HEAD~1              # Undo last commit (⚠️ careful!)
```

### View Differences
```bash
git diff                   # Compare working directory to staging
git diff --staged          # Compare staging to last commit
git diff main              # Compare to main branch
```

---

## Before Committing

Run tests and checks:

```bash
# Run tests
pytest tests/

# Format code
black src/

# Lint
pylint src/

# Then commit
git add .
git commit -m "feat: Your feature"
```

---

## PR Review Checklist

Before submitting a PR:

- [ ] Code tested locally
- [ ] Tests added/updated
- [ ] Code formatted with `black`
- [ ] Docstrings updated
- [ ] README/docs updated if needed
- [ ] No breaking changes to API
- [ ] Commit messages follow conventional commits

Example PR Description:
```
## Description
Adds dynamic instruction switching for routing analysis

## Changes
- Add `instructions_routing.md` with 7-phase routing engine
- Update agent to support `instruction_type` parameter
- Add `set_instruction_type()` method for runtime switching

## Testing
- Tested with real action 676893
- Verified both summary and routing modes
- All tests pass

## Validation
- Routing decision: Tech RoB | Service Availability ✓
- Fallback to summary mode works ✓
```

---

## Commit History Standards

All commits should:
1. Have clear, descriptive messages
2. Follow conventional commits format
3. Be logically grouped (one feature per commit when possible)
4. Include relevant context in the commit body for complex changes

Example good commit:
```bash
git commit -m "feat: Implement 7-phase routing analysis engine

- Phase 1: Data extraction and normalization
- Phase 2: Requestor classification (CSU/STU)
- Phase 3: Service-to-solution mapping
- Phase 5: Direct routing rules (milestone-driven)
- Phase 7: JSON + human-readable output

Tested with action 676893, routing to Tech RoB | Service Availability"
```

---

## Phase Roadmap

- ✅ **Phase 1**: Simple Model Interaction
- ✅ **Phase 2**: MCP Integration + Routing Analysis
- 🔲 **Phase 3**: Multi-Platform Deployment
  - Teams/M365 Copilot plugin
  - PowerBI custom functions
  - Web app integration
  
See [PHASE2_MCP_INTEGRATION.md](PHASE2_MCP_INTEGRATION.md) for details.

---

## Troubleshooting

### "fatal: not a git repository"
```bash
cd c:\src\techrob_action360_agent
git status
```

### Push rejected ("Updates were rejected")
```bash
git pull origin main         # Get latest changes
# Resolve conflicts if any
git push origin feat/branch
```

### Accidentally committed to main
```bash
git checkout main
git reset --soft HEAD~1     # Undo commit, keep changes staged
git checkout -b feat/new-feature
git commit -m "feat: Your changes"
```

### Need to switch branches
```bash
git checkout feat/your-branch
# or create and switch
git checkout -b feat/new-feature
```

---

## Next Steps

1. **Clone and setup**: `git clone https://github.com/ChrisKoenig/techrob-action360-agent.git`
2. **See QUICKSTART.md** for running the agent
3. **Explore config/instructions_routing.md** to understand routing logic
4. **Create a feature branch** for your changes
5. **Submit PR** with description of changes

Happy coding! 🚀
