# GitHub Minimum Reviewer Policy Setup

## How to Enable Minimum Reviewer Policy for Pull Requests

Follow these steps to require at least 1 reviewer before merging to `main` or `develop` branches:

### Step 1: Go to Repository Settings
1. Navigate to your GitHub repository: `https://github.com/your-username/nagp`
2. Click on **Settings** (top right)

### Step 2: Configure Branch Protection Rules
1. In the left sidebar, click **Branches**
2. Under "Branch protection rules", click **Add rule**

### Step 3: Add Rule for `main` Branch
1. **Branch name pattern**: `main`
2. Enable the following:
   - ✅ **Require pull request reviews before merging**
     - Set to **1** for minimum number of reviews
   - ✅ **Require status checks to pass before merging**
     - Search and select: `build-and-push` workflow
   - ✅ **Require branches to be up to date before merging**
3. Click **Create** or **Save changes**

### Step 4: Add Rule for `develop` Branch (Optional)
Repeat Step 3 with:
- **Branch name pattern**: `develop`
- Same requirements as main

### Result
Now all PRs targeting `main` or `develop` require:
- ✅ At least 1 reviewer approval before merge
- ✅ Build and push workflow passes
- ✅ Branch is up to date with base branch

## Verifying the Policy

1. Create a test branch: `git checkout -b test-feature`
2. Make a commit: `git add . && git commit -m "test"`
3. Push and create a PR: `git push origin test-feature`
4. Observe the PR now shows:
   - "1 review required"
   - Merge button is disabled until reviewed
5. Add a reviewer and they can approve/request changes

## Reviewer Management

To add specific reviewers:
1. Go to PR → **Reviewers** (right sidebar)
2. Select team members or specific people
3. Set as "Request" or assign based on preference

## Using CODEOWNERS (Advanced)

To automatically request reviewers, create `.github/CODEOWNERS`:

```
# Auto-request reviewers for specific paths
auth/ @username1
product/ @username1
cart/ @username2
order/ @username2
nagp-frontend/ @username3
```

Users with push access can auto-approve their own changes (configure in branch protection settings if desired).
