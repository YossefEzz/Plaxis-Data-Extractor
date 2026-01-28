# GitHub Upload Guide - Step by Step

## What is GitHub and Why We Use It

**GitHub** is a cloud platform that stores your code online, allowing:
- **Backup** - Your code is safe on GitHub servers
- **Sharing** - Others can easily access and use your project
- **Collaboration** - Multiple people can work on the same project
- **Version Control** - Track all changes made to your code

## Prerequisites

1. **GitHub Account** - Create free account at https://github.com/signup
2. **Git Installed** - Already done (you have .git folder)
3. **Your local repository** - Already initialized ✓

## Step-by-Step GitHub Upload

### Step 1: Create a GitHub Repository

1. Log in to https://github.com
2. Click the **+** icon in top-right corner
3. Select **New repository**
4. Fill in:
   - **Repository name:** `Plaxis-Data-Extractor`
   - **Description:** `Python tool to extract cross-section results from PLAXIS 2D models`
   - **Public** (so others can see and use it) or **Private** (only you)
   - Do NOT check "Initialize with README" (we already have one)
5. Click **Create repository**

### Step 2: Copy the Repository URL

After creating, GitHub shows a page with HTTPS URL like:
```
https://github.com/yourusername/Plaxis-Data-Extractor.git
```

Keep this URL handy - you'll use it next.

### Step 3: Connect Local Repository to GitHub

Run this command in PowerShell (replace with your actual URL):

```powershell
cd "d:\plx\Plaxis Data Extractor"
git remote add origin https://github.com/yourusername/Plaxis-Data-Extractor.git
```

**What this does:** Links your local folder to the GitHub online repository.

### Step 4: Push Code to GitHub

#### Option A: Using HTTPS (Simpler for first-time)

```powershell
git branch -M main
git push -u origin main
```

On first push, GitHub will ask for credentials:
- **Username:** Your GitHub username
- **Password:** Your GitHub personal access token (not your password!)

**To create a Personal Access Token:**
1. Go to GitHub Settings → Developer Settings → Personal access tokens
2. Click "Generate new token"
3. Check: `repo` (full control of private repositories)
4. Copy the token (shown once!)
5. Paste when Git asks for password

#### Option B: Using SSH (More secure, requires setup)

If you want SSH setup, follow: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

### Step 5: Verify Upload

Go to https://github.com/yourusername/Plaxis-Data-Extractor

You should see your files:
- ✓ wall.py
- ✓ requirements.txt
- ✓ README.md
- ✓ .gitignore

## How Others Will Use Your Project

### They see your repository on GitHub
```
↓
Click "Code" button
↓
Copy the URL
↓
In their PowerShell, run:
    git clone https://github.com/yourusername/Plaxis-Data-Extractor.git
↓
cd Plaxis-Data-Extractor
↓
pip install -r requirements.txt
↓
python wall.py
```

**It works on their computer because:**
1. `requirements.txt` tells pip what to install
2. Code uses dynamic paths (not hardcoded)
3. Code finds PLAXIS automatically
4. README explains setup

## Making Updates (Later)

After making changes to your code:

```powershell
cd "d:\plx\Plaxis Data Extractor"
git add .
git commit -m "Fixed bug in cross-section calculation"
git push
```

Your updates automatically appear on GitHub!

## Common Issues & Solutions

### "authentication failed"
- Double-check your Personal Access Token
- Ensure you copied the entire token (it's long)
- Delete saved credentials and try again

### "fatal: destination path already exists"
- You already have the repo locally
- Just use `git add . && git commit && git push`

### "error: src refspec main does not match any"
- Run: `git branch -M main` before push

## Repository Badges (Optional - Makes it Look Professional)

Add to your README.md:

```markdown
![Python Version](https://img.shields.io/badge/python-3.7+-blue)
![License](https://img.shields.io/badge/license-MIT-green)
```

## Summary

| Step | Action | Command |
|------|--------|---------|
| 1 | Create GitHub repo | Web interface |
| 2 | Get repo URL | Copy from GitHub |
| 3 | Connect local repo | `git remote add origin <URL>` |
| 4 | Push to GitHub | `git push -u origin main` |
| 5 | Verify | Visit GitHub URL |
| 6 | Update | `git push` after each commit |

## Why This Makes Code Portable

✓ **No absolute paths** - Uses relative paths and automatic detection
✓ **No external dependencies** - Everything listed in requirements.txt
✓ **No hardcoded credentials** - Prompts user for input
✓ **Cross-platform** - Works on any Windows with Python + PLAXIS
✓ **Version controlled** - Track changes and revert if needed
✓ **Cloud backup** - Safe on GitHub servers

---

**Questions?** GitHub has excellent guides at https://docs.github.com
