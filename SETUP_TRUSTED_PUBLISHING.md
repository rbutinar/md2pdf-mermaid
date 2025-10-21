# Setup Instructions for GitHub Actions Trusted Publishing

The GitHub workflow file has been created at `.github/workflows/publish.yml`.

## What I've Done (Automated)

✅ Created `.github/workflows/publish.yml` - GitHub Actions workflow for automated publishing

## What You Need to Do Manually

### Step 1: Configure Trusted Publisher on PyPI

1. **Log in to PyPI**: Go to https://pypi.org and log in with your account

2. **Navigate to Publishing Settings**: Visit https://pypi.org/manage/account/publishing/

3. **Add a New Pending Publisher** with these exact values:
   - **PyPI Project Name**: `md2pdf-mermaid`
   - **Owner**: `rbutinar` (your GitHub username)
   - **Repository name**: `md2pdf-mermaid`
   - **Workflow filename**: `publish.yml`
   - **Environment name**: `pypi`

4. **Save the configuration**

   Note: This creates a "pending publisher" which will automatically create/claim the project name on first successful publish.

### Step 2: Configure GitHub Environment (Optional but Recommended)

This adds an extra layer of security by requiring manual approval before publishing:

1. Go to your GitHub repository: https://github.com/rbutinar/md2pdf-mermaid

2. Click **Settings** → **Environments** → **New environment**

3. Name it: `pypi`

4. Add **Environment protection rules**:
   - ✅ Check "Required reviewers"
   - Add yourself (or trusted collaborators) as reviewers
   - This means you'll need to manually approve each release before it publishes

5. **Save protection rules**

### Step 3: Test the Setup

Once you've completed Steps 1 and 2, test the workflow:

1. Make sure all your version strings are updated (see `claude.md`)

2. Commit the workflow file:
   ```bash
   git add .github/workflows/publish.yml
   git commit -m "Add GitHub Actions trusted publishing workflow"
   git push
   ```

3. Create and push a test tag:
   ```bash
   git tag v1.2.2
   git push origin v1.2.2
   ```

4. Check GitHub Actions:
   - Go to https://github.com/rbutinar/md2pdf-mermaid/actions
   - You should see the workflow running
   - If you configured the environment with required reviewers, you'll need to approve it
   - The workflow will build and publish to PyPI automatically

## How It Works After Setup

Once configured, publishing new versions is simple:

1. Update version strings in code
2. Commit changes
3. Create and push a version tag:
   ```bash
   git tag v1.3.0
   git push origin v1.3.0
   ```
4. GitHub Actions automatically:
   - Builds the package
   - Waits for your approval (if configured)
   - Publishes to PyPI using secure OIDC authentication
   - No tokens needed!

## Troubleshooting

**If the workflow fails with "Trusted publishing exchange failure":**
- Double-check that the PyPI pending publisher configuration matches exactly:
  - Repository owner: `rbutinar`
  - Repository name: `md2pdf-mermaid`
  - Workflow filename: `publish.yml`
  - Environment name: `pypi`

**If you don't see the workflow running:**
- Make sure you pushed the tag (not just created it locally)
- Verify the tag name starts with `v` (e.g., `v1.2.2`)

**If you need to test without publishing to production:**
- Consider setting up TestPyPI first (see `claude.md` for instructions)
