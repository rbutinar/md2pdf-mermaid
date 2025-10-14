# Publishing md2pdf-mermaid to PyPI

This guide explains how to publish md2pdf-mermaid to the official Python Package Index (PyPI).

## 📛 Important: Package Name vs Module Name

**This package uses different names for different purposes** (this is common in Python):

- **PyPI Package Name**: `md2pdf-mermaid` (for `pip install`)
- **Python Module Name**: `md2pdf` (for `import md2pdf`)
- **Command Name**: `md2pdf` (CLI tool)

**Why not just `md2pdf`?**
- The name `md2pdf` is **already taken** on PyPI (by Julien Maupetit, v1.0.1, 2023)
- `md2pdf-mermaid` is more descriptive (highlights Mermaid diagram support)
- Avoids conflicts while keeping clean Python imports

**Similar examples in Python ecosystem:**
- `pip install pillow` → `import PIL`
- `pip install beautifulsoup4` → `import bs4`
- `pip install scikit-learn` → `import sklearn`

**For your users:**
```bash
# Installation
pip install md2pdf-mermaid

# Usage in Python
import md2pdf
from md2pdf import convert_markdown_to_pdf

# Command line
md2pdf document.md
```

## ✅ Should You Publish to PyPI?

### Pros:
- ✅ **Easier installation**: Users can do `pip install md2pdf-mermaid` instead of `pip install git+https://...`
- ✅ **Version management**: PyPI handles versioning automatically
- ✅ **Discoverability**: People can find your package searching on PyPI
- ✅ **Professional**: Shows the package is maintained and stable
- ✅ **Better for requirements.txt**: Cleaner dependency specifications
- ✅ **CI/CD friendly**: No need for git URLs in automated pipelines

### Cons:
- ⚠️ **Name reservation**: Once published, the name `md2pdf-mermaid` is yours
- ⚠️ **Maintenance responsibility**: Users expect updates and bug fixes
- ⚠️ **Can't unpublish**: You can only "yank" versions, not delete them
- ⚠️ **Public visibility**: Anyone can see and use your code (already true with GitHub)

### Recommendation:
**YES, publish it!** The package is:
- ✅ Well-documented (README, WSL_SETUP)
- ✅ Tested and working
- ✅ Has clear use cases
- ✅ Follows Python packaging standards
- ✅ Already has a professional setup.py

---

## 📋 Pre-Publishing Checklist

Before publishing, ensure:

- [ ] Version number is correct in `setup.py` (currently 1.0.0)
- [ ] `author_email` is filled in `setup.py` (currently empty)
- [ ] README.md is complete and accurate
- [ ] LICENSE file exists (MIT license present ✅)
- [ ] All tests pass (if any)
- [ ] Code is committed and pushed to GitHub
- [ ] You have a PyPI account

---

## 🔧 Setup Steps

### 1. Create PyPI Account

1. Go to https://pypi.org/account/register/
2. Create account (use your professional email)
3. Verify email address

### 2. Create Test PyPI Account (Optional but Recommended)

1. Go to https://test.pypi.org/account/register/
2. Create account (can use same email)
3. This allows testing uploads before going live

### 3. Set Up API Tokens

**PyPI (Production)**:
1. Login to https://pypi.org
2. Go to Account Settings → API tokens
3. Click "Add API token"
4. Scope: "Entire account" or "Project: md2pdf-mermaid" (after first upload)
5. **Save the token** - you won't see it again!

**Test PyPI** (optional):
1. Login to https://test.pypi.org
2. Follow same steps as above

### 4. Configure pip

Create/edit `~/.pypirc`:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-AgEIc... (your token here)

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgEIc... (your test token here)
```

**Important**: Keep this file secure! Add to `.gitignore` if in project directory.

---

## 📦 Publishing Process

### Update Version (if needed)

Edit `setup.py` line 14:

```python
version="1.0.1",  # Increment for new releases
```

### Add author_email

Edit `setup.py` line 16:

```python
author_email="your.email@example.com",
```

### Install Build Tools

```bash
pip install --upgrade build twine
```

### Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build distribution packages
python -m build
```

This creates:
- `dist/md2pdf_mermaid-1.0.0-py3-none-any.whl` (wheel)
- `dist/md2pdf-mermaid-1.0.0.tar.gz` (source)

### Test Build Locally (Optional)

```bash
# Install from local wheel
pip install dist/md2pdf_mermaid-1.0.0-py3-none-any.whl

# Test it works
md2pdf --help
```

### Upload to Test PyPI (Recommended First Time)

```bash
# Upload to test.pypi.org
python -m twine upload --repository testpypi dist/*

# Test installation from Test PyPI
pip install --index-url https://test.pypi.org/simple/ md2pdf-mermaid
```

### Upload to Production PyPI

```bash
# Upload to pypi.org (LIVE!)
python -m twine upload dist/*
```

You'll see:
```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading md2pdf_mermaid-1.0.0-py3-none-any.whl
Uploading md2pdf-mermaid-1.0.0.tar.gz
```

### Verify Publication

1. Visit https://pypi.org/project/md2pdf-mermaid/
2. Check version, description, README rendering
3. Test installation:
   ```bash
   pip install md2pdf-mermaid
   ```

---

## 🔄 Releasing New Versions

For updates:

1. **Update version** in `setup.py`
   ```python
   version="1.0.1",  # or 1.1.0 for features, 2.0.0 for breaking changes
   ```

2. **Update CHANGELOG.md** with changes

3. **Commit and tag**:
   ```bash
   git add setup.py CHANGELOG.md
   git commit -m "Release v1.0.1"
   git tag v1.0.1
   git push origin master --tags
   ```

4. **Build and upload**:
   ```bash
   rm -rf dist/
   python -m build
   python -m twine upload dist/*
   ```

---

## 📝 After Publishing

### Update README Installation Section

Change from:
```bash
pip install git+https://github.com/rbutinar/md2pdf-mermaid.git
```

To:
```bash
pip install md2pdf-mermaid
```

### Add PyPI Badge

Add to README.md:
```markdown
[![PyPI version](https://badge.fury.io/py/md2pdf-mermaid.svg)](https://badge.fury.io/py/md2pdf-mermaid)
```

### Monitor Package

- Check download stats: https://pypistats.org/packages/md2pdf-mermaid
- Watch GitHub issues for bug reports
- Respond to PyPI project page comments

---

## 🐛 Troubleshooting

### "Package name already exists"

If `md2pdf-mermaid` is taken by someone else, choose a different one in `setup.py`:
```python
name="md2pdf-mermaid-rb",  # Add your initials
# or
name="md2pdf-with-mermaid",  # Alternative naming
```

**Note**: As of 2025-10-14, `md2pdf-mermaid` is available on PyPI ✅

### "Invalid credentials"

- Check your API token in `~/.pypirc`
- Make sure token starts with `pypi-`
- Token must be for the correct repository (pypi vs testpypi)

### "File already exists"

You can't re-upload the same version. Increment version number.

### README not rendering on PyPI

- Ensure `long_description_content_type="text/markdown"` in setup.py
- Validate with: `python -m readme_renderer README.md`

---

## 🎯 Quick Command Reference

```bash
# One-time setup
pip install --upgrade build twine

# For each release
rm -rf dist/ build/ *.egg-info
python -m build
python -m twine upload --repository testpypi dist/*  # Test first
python -m twine upload dist/*                        # Then production

# Verify
pip install md2pdf-mermaid
md2pdf --version
```

---

## 📊 Current Status

- **Package name**: md2pdf-mermaid (available ✅)
- **Current version**: 1.0.0
- **License**: MIT ✅
- **Setup.py**: Ready ✅
- **README**: Professional ✅
- **Documentation**: Complete ✅

**Ready to publish!** 🚀

---

## 🔗 Resources

- PyPI: https://pypi.org
- Test PyPI: https://test.pypi.org
- Packaging Guide: https://packaging.python.org/tutorials/packaging-projects/
- Twine Docs: https://twine.readthedocs.io/
- Semantic Versioning: https://semver.org/

---

**Questions?**
- PyPI Help: https://pypi.org/help/
- Python Packaging Discord: https://discord.gg/pypa
