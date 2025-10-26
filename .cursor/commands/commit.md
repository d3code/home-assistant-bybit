---
description: Analyze staged changes and generate a conventional commit message automatically
---

# Generate and Commit with Conventional Commit Message

You are creating an intelligent conventional commit message by analyzing the staged changes in the current project.

## Step 1: Navigate to Project Root Directory

First, ensure we're in the project root directory:

Run: `git rev-parse --show-toplevel`

This will return the absolute path to the git repository root. Store this path.

Then run: `cd <git-root-path>`

This ensures all subsequent git operations happen from the project root.

## Step 2: Stage All Changes

Run: `git add .`

This stages all modified, new, and deleted files in the working directory.

## Step 3: Check for Staged Changes

Run: `git diff --cached --stat` and `git diff --cached`

If there are no staged changes after running `git add .`, inform the user:
```
No changes to commit. Working directory is clean.
```

And exit.

## Step 4: Analyze the Changes

Examine the git diff output and determine:

### A. Commit Type

Based on the changes, select the most appropriate type:

- **feat**: New features, new functionality added
  - New files in `/internal/`, `/app/`, `/components/`
  - New API endpoints, new pages, new components
  - New functionality in existing files

- **fix**: Bug fixes
  - Error handling improvements
  - Fixing broken functionality
  - Correcting logic errors

- **docs**: Documentation only
  - Changes only to `.md` files
  - Updates to `/documentation/`
  - README updates
  - Code comments (if substantial)

- **style**: Formatting, whitespace, linting
  - Code formatting changes
  - Eslint/prettier fixes
  - No logic changes

- **refactor**: Code restructuring without changing behavior
  - Moving code between files
  - Renaming variables/functions
  - Extracting functions/components
  - Code organization improvements

- **perf**: Performance improvements
  - Optimization changes
  - Caching improvements
  - Query optimization

- **test**: Test additions or modifications
  - New test files
  - Updates to existing tests
  - Test configuration

- **build**: Build system, dependencies
  - `package.json`, `go.mod` changes
  - Dependency updates
  - Build configuration

- **ci**: CI/CD configuration
  - `.github/workflows/` changes
  - Docker configuration
  - Deployment scripts

- **chore**: Maintenance, configs
  - Configuration files
  - Tooling updates
  - Cleanup tasks

### B. Scope

Determine scope based on affected directories/components:

- **backend**: Changes in `/backend/`, `/server/`, `/api/`
- **frontend**: Changes in `/frontend/`, `/client/`, `/web/`, `/app/`
- **docs**: Changes in `/documentation/`, `/docs/`
- **api**: API endpoint changes
- **auth**: Authentication related
- **ui**: UI components, `/components/`, `/src/components/`
- **db**: Database migrations/schema, `/migrations/`
- **config**: Configuration files, `/config/`
- **tests**: Test files, `/tests/`, `/__tests__/`
- **scripts**: Build scripts, `/scripts/`
- **deps**: Dependency updates, `package.json`, `go.mod`, `requirements.txt`

Use the most specific scope. If changes span multiple areas, choose the primary one or omit scope.

### C. Description

Generate a concise description (under 72 characters):
- Use imperative mood: "add", "fix", "update", "remove", "refactor"
- Lowercase, no period at end
- Be specific but brief
- Focus on WHAT changed, not HOW

Examples:
- "add user authentication endpoint"
- "fix memory leak in email parser"
- "update installation guide with go 1.25"
- "refactor domain validation logic"

### D. Body (Optional)

If changes are complex, generate a body that explains:
- WHY the change was made
- WHAT problem it solves
- Any important context
- Wrap at 72 characters

### E. Breaking Changes

Detect breaking changes:
- API signature changes
- Removed functionality
- Changed behavior that affects clients
- Database schema changes requiring migration

If breaking change detected, add `!` after type/scope and include `BREAKING CHANGE:` footer.

## Step 5: Generate Commit Message

Format the message:

```
<type>(<scope>): <description>

<body if needed>

<BREAKING CHANGE: description if applicable>
```

## Step 6: Show Analysis and Commit

Display analysis and automatically commit:

```
📊 Analysis:
- Files changed: <count>
- Commit type: <type>
- Scope: <scope>
- Breaking change: <yes/no>

📝 Committing with message:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<formatted commit message>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Then execute: `git commit -m "<message>"` (or `git commit -m "<header>" -m "<body>"` if body exists)

## Step 7: Confirm Success

After successful commit:
```
✅ Committed successfully!

Commit: <hash>
Files changed: <count>
Insertions: <count>
Deletions: <count>
```

## Analysis Guidelines

### For Backend Changes
- New services → `feat(backend): add <service> service`
- API endpoints → `feat(api): add <endpoint>` or `fix(api): correct <issue>`
- Database changes → `feat(db): add <table> schema` or `build(db): update schema`
- Configuration → `chore(config): update <setting>`

### For Frontend Changes
- New pages → `feat(ui): add <page> page`
- New components → `feat(ui): add <component> component`
- Component updates → `fix(ui): resolve <issue>` or `refactor(ui): improve <component>`
- Style changes → `style(ui): format <component>`

### For Documentation
- Documentation updates → `docs: update <topic>`
- README changes → `docs: update readme with <info>`
- Setup guides → `docs(setup): add <guide>`

### For Multiple File Types
Choose primary type based on most significant change:
- If adding feature code + tests → `feat` (tests are supporting)
- If updating code + docs → use code type (docs are supporting)
- If only docs + config → `docs` or `chore`

## Example Scenarios

### Scenario 1: New Authentication Feature
Files: `src/auth/login.js`, `src/auth/register.js` (new)
Diff: Shows new functions for login, register, JWT generation

Generated:
```
feat(auth): add user authentication endpoints

Implements login and registration endpoints with JWT token
generation. Includes password hashing and token validation.
```

### Scenario 2: Bug Fix in Component
Files: `src/components/UserList.js`
Diff: Fixes memory leak by properly cleaning up event listeners

Generated:
```
fix(ui): prevent memory leak in user list component

Component was not removing event listeners on unmount,
causing memory to grow unbounded over time.
```

### Scenario 3: Documentation Update
Files: `README.md`, `docs/setup.md`
Diff: Updates installation instructions and adds new features

Generated:
```
docs: update installation guide and feature list

Added new setup instructions for Docker and updated
feature list to include recent additions.
```

### Scenario 4: Multiple File Changes
Files: `package.json`, `src/utils/helpers.js`, `tests/helpers.test.js`
Diff: Added new utility functions with tests

Generated:
```
feat(utils): add helper functions for data processing

Added formatDate, validateEmail, and sanitizeInput functions
with comprehensive test coverage.
```

## Important Rules

1. **Be specific**: Generic messages like "update code" are not helpful
2. **Use imperative mood**: "add" not "added" or "adds"
3. **Keep header under 72 chars**: Break longer descriptions into body
4. **One commit = one logical change**: If diff shows unrelated changes, suggest splitting
5. **Respect conventions**: Follow project patterns and terminology
6. **Context matters**: Consider what developers will want to know in the future

Now analyze the staged changes and generate an appropriate conventional commit message.
