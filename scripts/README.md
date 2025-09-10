# Version Management Scripts

## Automated Version Bumping

This project supports automated version management through GitHub Actions and manual scripts.

### GitHub Actions (Recommended)

The automated release workflow (`.github/workflows/release.yml`) will automatically:

1. **Detect version bump type** from commit messages:
   - `feat:` or `[minor]` → minor version bump (0.1.2 → 0.2.0)
   - `BREAKING CHANGE` or `[major]` → major version bump (0.1.2 → 1.0.0)
   - Everything else → patch version bump (0.1.2 → 0.1.3)

2. **Automatically bump version** in both `pyproject.toml` and `flask_react/__init__.py`
3. **Create Git tag** and push changes
4. **Create GitHub release**
5. **Publish to PyPI**

### Commit Message Examples

```bash
# Patch release (0.1.2 → 0.1.3)
git commit -m "fix: resolve rendering issue with UserProfile component"

# Minor release (0.1.2 → 0.2.0)  
git commit -m "feat: add new React component caching system"

# Major release (0.1.2 → 1.0.0)
git commit -m "feat: redesign API

BREAKING CHANGE: ReactRenderer constructor now requires components_dir parameter"
```

### Manual Version Bumping

Use the `bump_version.py` script for local development:

```bash
# Bump patch version (0.1.2 → 0.1.3)
python scripts/bump_version.py patch

# Bump minor version (0.1.2 → 0.2.0)
python scripts/bump_version.py minor --push

# Bump major version (0.1.2 → 1.0.0)
python scripts/bump_version.py major --push
```

### Configuration

Version management is configured in `.bumpversion.cfg`:

- Automatically updates `pyproject.toml`
- Automatically updates `flask_react/__init__.py`
- Creates Git commits and tags
- Supports semantic versioning

### Workflow Summary

1. **Development**: Make your changes and commit with descriptive messages
2. **Automatic**: Push to main branch - GitHub Actions handles the rest
3. **Manual**: Use `python scripts/bump_version.py [type]` if needed
