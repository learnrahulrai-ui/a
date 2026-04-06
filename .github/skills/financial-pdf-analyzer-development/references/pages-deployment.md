# Deployment to GitHub Pages

## Overview

This repository includes a GitHub Actions workflow (`.github/workflows/pages.yml`) that automatically publishes a static preview to GitHub Pages whenever you push to `main`, `master`, or `work` branches.

## How It Works

1. **Trigger**: Push changes to `preview/` or the workflow file itself
2. **Build**: GitHub Actions checks out the repo and uploads the `preview/` folder
3. **Deploy**: Pages publishes to `https://<owner>.github.io/<repo>/`

The **preview page is static-only**. It explains that full app functionality (PDF upload + AI analysis) requires running in Codespaces.

## Manual Deployment

```bash
# Ensure changes are committed
git add .
git commit -m "Update preview content"

# Push to main (triggers the workflow)
git push origin main
```

Check deployment status:
1. Go to `https://github.com/learnrahulrai-ui/a`
2. Click **Actions** tab
3. Look for "Deploy preview to GitHub Pages" workflow
4. Wait ~2 minutes for completion

## Verifying Your Site

Once deployed, visit:
```
https://learnrahulrai-ui.github.io/a/
```

Should show:
- Title: "Financial PDF Analyzer (Preview)"
- Note explaining that Pages is static-only
- Link/instructions to use Codespaces for full functionality

## Repository Settings

Verify Pages is enabled:

1. Go to **Settings → Pages**
2. Ensure **Source** is set to **GitHub Actions**
3. Custom domain (optional): Add if you have one

## Customizing the Preview Page

Edit `preview/index.html`:

```html
<!doctype html>
<html lang="en">
  <head>
    <title>Your Custom Title</title>
  </head>
  <body>
    <h1>Your Custom Content</h1>
    <p>Preview explanation...</p>
  </body>
</html>
```

After edits:
```bash
git add preview/index.html
git commit -m "Update preview page"
git push origin main
```

The workflow will redeploy automatically.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| "There isn't a GitHub Pages site here" | Workflow hasn't run yet | Wait 2-3 minutes; hardrefresh `Ctrl+Shift+R` |
| Pages not updating | Changes not on `main` branch | Push to `main`, not feature branch |
| Workflow failing | Invalid syntax in HTML/workflow | Check **Actions** tab for error logs |
| Custom domain not working | Pages settings mismatch | Update **Settings → Pages → Custom domain** |

## File Structure for Pages

```
preview/
└── index.html       # Main page (required)
styles.css          # CSS (optional, reference in HTML)
images/             # Images (optional)
```

All files in `preview/` are published to the root of the Pages URL.

## Example: Add a Stylesheet

1. Create `preview/styles.css`:
   ```css
   body { font-family: Arial; background: #f0f0f0; }
   ```

2. Reference in `preview/index.html`:
   ```html
   <link rel="stylesheet" href="styles.css">
   ```

3. Push:
   ```bash
   git add preview/
   git commit -m "Add CSS styling to preview"
   git push origin main
   ```

## Full App Deployment (Codespaces)

Pages is static-only. To run the full Flask app:

1. Click **Code → Codespaces → Create codespace on branch**
2. Set up environment variables
3. Run `python app.py`
4. Open forwarded port 8000

## URL Structure

- **Main site**: `https://learnrahulrai-ui.github.io/a/`
- **If custom domain**: `https://yourdomain.com/`
- **Subdirectory**: Not applicable (repo is the root)

## Security Notes

- GitHub Pages is **public** — anything in `preview/` is visible to the internet
- Don't commit API keys, secrets, or private files to `preview/`
- Use environment variables for sensitive config in the Flask app backend

---

**For more**: [GitHub Pages Documentation](https://docs.github.com/en/pages)
