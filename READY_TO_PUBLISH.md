# 🚀 Ready to Publish to PyPI!

All preparation is complete. The package is **ready to be published**.

## ✅ What's Been Done

- ✅ Build files created and tested
- ✅ Metadata validated (twine check PASSED)
- ✅ Modern pyproject.toml configuration
- ✅ Fixed setuptools/twine compatibility
- ✅ Author email configured
- ✅ All files committed to GitHub

## 📦 Distribution Files Ready

```
dist/
├── md2pdf_mermaid-1.0.0-py3-none-any.whl (12K)
└── md2pdf_mermaid-1.0.0.tar.gz (13K)
```

Both files have **PASSED** twine validation!

---

## 🔐 Step 1: Get PyPI Credentials

If you don't have a PyPI account yet:

1. **Create account**: https://pypi.org/account/register/
2. **Verify email**
3. **Create API token**:
   - Go to: https://pypi.org/manage/account/
   - Click "API tokens" → "Add API token"
   - Name: "md2pdf-mermaid upload"
   - Scope: "Entire account" (or "Project: md2pdf-mermaid" after first upload)
   - **COPY THE TOKEN** (starts with `pypi-AgEI...`)
   - You won't see it again!

---

## 🚀 Step 2: Upload to PyPI

### Option A: Manual Upload (One Time)

Open your terminal and run:

```bash
cd /mnt/c/codebase/md2pdf-mermaid
python3.exe -m twine upload dist/*
```

When prompted:
```
Username: __token__
Password: (paste your PyPI token here)
```

### Option B: Save Credentials (Recommended)

Create `~/.pypirc`:

```bash
cat > ~/.pypirc <<'EOF'
[pypi]
username = __token__
password = pypi-AgEI... (your actual token)
EOF

chmod 600 ~/.pypirc  # Secure the file
```

Then upload:

```bash
cd /mnt/c/codebase/md2pdf-mermaid
python3.exe -m twine upload dist/*
```

No password prompt!

---

## ✨ Step 3: Verify Publication

After successful upload, you'll see:

```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading md2pdf_mermaid-1.0.0-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Uploading md2pdf_mermaid-1.0.0.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

View at:
https://pypi.org/project/md2pdf-mermaid/1.0.0/
```

**Check your package:**
1. Visit: https://pypi.org/project/md2pdf-mermaid/
2. Verify README renders correctly
3. Check metadata (author, license, etc.)

**Test installation:**
```bash
# Create fresh environment
python3.exe -m venv test_env
test_env/Scripts/pip.exe install md2pdf-mermaid
test_env/Scripts/md2pdf.exe --help
```

---

## 🎉 After Publishing

### Update Installation Instructions

Users can now install with:
```bash
pip install md2pdf-mermaid
```

Instead of:
```bash
pip install git+https://github.com/rbutinar/md2pdf-mermaid.git
```

### Add PyPI Badge to README

Add this to the top of README.md:

```markdown
[![PyPI version](https://badge.fury.io/py/md2pdf-mermaid.svg)](https://pypi.org/project/md2pdf-mermaid/)
[![Python versions](https://img.shields.io/pypi/pyversions/md2pdf-mermaid.svg)](https://pypi.org/project/md2pdf-mermaid/)
[![Downloads](https://pepy.tech/badge/md2pdf-mermaid)](https://pepy.tech/project/md2pdf-mermaid)
```

### Monitor Your Package

- **Download stats**: https://pypistats.org/packages/md2pdf-mermaid
- **Package page**: https://pypi.org/project/md2pdf-mermaid/
- **GitHub issues**: https://github.com/rbutinar/md2pdf-mermaid/issues

---

## 🔄 Publishing Updates (Future Versions)

When you release v1.0.1, v1.1.0, etc.:

1. **Update version** in `pyproject.toml`:
   ```toml
   version = "1.0.1"
   ```

2. **Update CHANGELOG.md**

3. **Commit and tag**:
   ```bash
   git add pyproject.toml CHANGELOG.md
   git commit -m "Release v1.0.1"
   git tag v1.0.1
   git push origin master --tags
   ```

4. **Build and upload**:
   ```bash
   rm -rf dist/ build/ *.egg-info
   python3.exe -m build
   python3.exe -m twine upload dist/*
   ```

---

## ⚠️ Important Notes

- **Can't delete versions**: Once uploaded, you can only "yank" them (hide from pip)
- **Can't re-upload same version**: Must increment version number for any changes
- **License is permanent**: MIT license can't be changed for existing versions
- **Email is public**: roberto.butinar@gmail.com will be visible on PyPI

---

## 🐛 Troubleshooting

### "File already exists"
You already uploaded this version. Increment version in `pyproject.toml`.

### "Invalid credentials"
- Check token starts with `pypi-`
- Make sure you're using `__token__` as username
- Token might be expired, create a new one

### "Package name already taken"
Someone else registered `md2pdf-mermaid`. Choose a different name in `pyproject.toml`.

**Note**: As of 2025-10-14, `md2pdf-mermaid` is **available** ✅

---

## 📊 Current Status

- **Package name**: md2pdf-mermaid ✅
- **Version**: 1.0.0
- **Build status**: Ready ✅
- **Validation**: Passed ✅
- **Available on PyPI**: Not yet (waiting for your upload)
- **Distribution files**: In `dist/` directory

---

## 🎯 Ready to Go!

Everything is prepared. Just run:

```bash
cd /mnt/c/codebase/md2pdf-mermaid
python3.exe -m twine upload dist/*
```

And follow the prompts!

Good luck! 🚀
