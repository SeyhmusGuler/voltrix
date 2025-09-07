# Dynamic Versioning Setup for Voltrix

This project uses `setuptools-scm` for automatic version management based on git tags and commits.

## How it works

1. **Manual version control**: Set major.minor versions manually using git tags
2. **Automatic patch increment**: The patch number (3rd component) is automatically incremented based on commits to the trunk branch

## Version Format

- **Development versions**: `major.minor.patch.devN+gHASH` (e.g., `1.2.3.dev5+g1a2b3c4`)
- **Release versions**: `major.minor.patch` (e.g., `1.2.3`)

## Setting up versions

### Initial setup (if no tags exist)
```bash
# Set the initial version tag
git tag v0.1.0
git push origin v0.1.0
```

### Creating a new release
```bash
# For a patch release (automatically determined by commits)
git tag v0.1.1
git push origin v0.1.1

# For a minor release
git tag v0.2.0
git push origin v0.2.0

# For a major release
git tag v1.0.0
git push origin v1.0.0
```

### Development workflow

1. Work on the `trunk` branch
2. Each commit automatically increments the development version
3. When ready for release, create and push a tag
4. The tag becomes the official release version

## Checking the current version

```bash
# In development (with package installed in editable mode)
python -c "import voltrix; print(voltrix.__version__)"

# Or using setuptools-scm directly
python -m setuptools_scm
```

## Installation for development

```bash
# Install in editable mode to get dynamic versioning
pip install -e .

# Or with dev dependencies
pip install -e .[dev]
```

## Notes

- The version is automatically written to `src/voltrix/_version.py` during build/install
- If the `_version.py` file doesn't exist (e.g., in a fresh clone), the package falls back to `0.0.0.dev0`
- The version calculation is based on the latest git tag and the number of commits since that tag
