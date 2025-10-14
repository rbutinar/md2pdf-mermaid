# Publishing Guide for md2pdf-mermaid

How to publish this repository to GitHub/Azure DevOps and use it in your projects.

---

## 🚀 Step 1: Create Remote Repository

### Option A: GitHub

1. Go to https://github.com/new
2. Repository name: `md2pdf-mermaid`
3. Description: "Markdown to PDF converter with Mermaid diagram support"
4. Visibility: Private (or Public)
5. Click "Create repository"

### Option B: Azure DevOps

1. Go to your Azure DevOps organization
2. Create new project or go to existing project
3. Go to Repos → Files → New Repository
4. Name: `md2pdf-mermaid`
5. Create

---

## 📤 Step 2: Push to Remote

### For GitHub:

```bash
# Add remote
git remote add origin https://github.com/rbutinar/md2pdf-mermaid.git

# Push code and tags
git push -u origin master
git push origin v1.0.0
```

### For Azure DevOps:

```bash
# Add remote
git remote add origin https://rbutinar@dev.azure.com/rbutinar/project/_git/md2pdf-mermaid

# Push code and tags
git push -u origin master
git push origin v1.0.0
```

---

## 📦 Step 3: Install in Your Projects

### From GitHub:

```bash
pip install git+https://github.com/rbutinar/md2pdf-mermaid.git@v1.0.0
```

### From Azure DevOps:

```bash
# Using Personal Access Token (PAT)
pip install git+https://YOUR_PAT@dev.azure.com/rbutinar/project/_git/md2pdf-mermaid@v1.0.0
```

### Install Playwright Browser:

```bash
playwright install chromium
```

---

## 🔧 Step 4: Update Your Projects

### In your project:

```bash
cd /path/to/your/project

# Add to requirements.txt
echo "md2pdf-mermaid @ git+https://github.com/rbutinar/md2pdf-mermaid.git@v1.0.0" >> requirements.txt

# Install
pip install -r requirements.txt
playwright install chromium

# Remove old utils (now in package)
rm utils/md_to_pdf_simple.py
rm utils/mermaid_renderer.py
rm utils/convert_to_pdf.sh
```

### Usage example:

```python
from md2pdf import convert_markdown_to_pdf

with open('docs/your_document.md') as f:
    content = f.read()

convert_markdown_to_pdf(content, 'output.pdf', title='Your Document')
```

---

## 🔄 Step 5: Making Updates

When you need to update the library:

```bash
cd /mnt/c/codebase/md2pdf-mermaid

# Make changes to code
# ... edit files ...

# Update version in setup.py and __init__.py
# version="1.1.0"

# Update CHANGELOG.md

# Commit changes
git add .
git commit -m "feat: add new feature"

# Tag new version
git tag -a v1.1.0 -m "Release v1.1.0"

# Push
git push origin master
git push origin v1.1.0
```

### Update in projects:

```bash
# Update to new version
pip install --upgrade git+https://github.com/rbutinar/md2pdf-mermaid.git@v1.1.0

# Or update requirements.txt and reinstall
pip install -r requirements.txt --upgrade
```

---

## 🎯 Step 6: Migration Checklist for Existing Projects

For each project using the old `utils/` approach:

- [ ] Add md2pdf-mermaid to requirements.txt
- [ ] Install package: `pip install git+https://...`
- [ ] Install Playwright: `playwright install chromium`
- [ ] Update import statements:
  ```python
  # OLD
  from md_to_pdf_simple import convert_markdown_to_pdf

  # NEW
  from md2pdf import convert_markdown_to_pdf
  ```
- [ ] Test conversion works
- [ ] Remove old utils files:
  - `utils/md_to_pdf_simple.py`
  - `utils/mermaid_renderer.py`
  - `utils/convert_to_pdf.sh`
  - `utils/README.md` (if only for PDF conversion)
- [ ] Update documentation if needed
- [ ] Commit changes

---

## 📝 Version Management

### Semantic Versioning:

- **v1.0.0** → **v1.0.1**: Bug fix (backward compatible)
- **v1.0.0** → **v1.1.0**: New feature (backward compatible)
- **v1.0.0** → **v2.0.0**: Breaking change (not backward compatible)

### Pinning Versions:

**Production projects**: Pin to specific version
```txt
md2pdf-mermaid @ git+https://github.com/rbutinar/md2pdf-mermaid.git@v1.0.0
```

**Development projects**: Use latest
```txt
md2pdf-mermaid @ git+https://github.com/rbutinar/md2pdf-mermaid.git
```

---

## 🔐 Private Repository Access

### Using SSH (Recommended):

```bash
# Generate SSH key if needed
ssh-keygen -t ed25519 -C "your.email@company.com"

# Add to GitHub/Azure DevOps
cat ~/.ssh/id_ed25519.pub  # Copy this

# Install using SSH
pip install git+ssh://git@github.com/rbutinar/md2pdf-mermaid.git@v1.0.0
```

### Using Personal Access Token:

```bash
# GitHub
pip install git+https://YOUR_TOKEN@github.com/rbutinar/md2pdf-mermaid.git@v1.0.0

# Azure DevOps
pip install git+https://YOUR_PAT@dev.azure.com/rbutinar/project/_git/md2pdf-mermaid@v1.0.0
```

### Using Environment Variable:

```bash
# Set token
export GIT_TOKEN="your_token_here"

# requirements.txt
md2pdf-mermaid @ git+https://${GIT_TOKEN}@github.com/rbutinar/md2pdf-mermaid.git@v1.0.0
```

---

## 🐳 Docker Configuration

If using Docker in projects:

```dockerfile
FROM python:3.11-slim

# Install git for pip install from git
RUN apt-get update && apt-get install -y git

# Install package
RUN pip install git+https://github.com/rbutinar/md2pdf-mermaid.git@v1.0.0

# Install Playwright browser
RUN playwright install chromium --with-deps

# Your project code
COPY . /app
WORKDIR /app
```

---

## ✅ Verification

After publishing and installing:

```bash
# Verify installation
python -c "from md2pdf import convert_markdown_to_pdf; print('OK')"

# Check version
python -c "from md2pdf import __version__; print(__version__)"

# Test conversion
md2pdf --version
md2pdf TEST_DOCUMENT.md
```

---

## 📊 Usage Statistics

Track adoption across your projects:

1. **Project A**: ✓ Ready to migrate
2. **Project B**: ✓ Ready to migrate
3. Other projects: Add as needed

---

## 🆘 Support

If issues arise:

1. Check repository is accessible: `git clone https://...`
2. Check Python version: `python --version` (need 3.8+)
3. Check Playwright installed: `playwright --version`
4. Open issue: https://github.com/rbutinar/md2pdf-mermaid/issues

---

**Repository Ready for Publishing!** 🎉

**Location**: `/mnt/c/codebase/md2pdf-mermaid/`
**Version**: v1.0.0
**Status**: Tested and Working ✓
