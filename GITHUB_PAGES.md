# GitHub Pages Deployment Guide

This repository is configured to deploy the PAV Sheet Merger web interface to GitHub Pages automatically.

## Enabling GitHub Pages

To enable GitHub Pages for this repository, the repository owner needs to:

1. Go to the repository Settings
2. Navigate to "Pages" in the left sidebar
3. Under "Build and deployment":
   - Source: Select "GitHub Actions"
4. Save the settings

Once enabled, the workflow will automatically deploy the site when changes are pushed to the `main` branch.

## Accessing the Web Interface

After deployment, the web interface will be available at:
```
https://rohilkohli.github.io/PAV-sheet-merger/
```

## How It Works

### GitHub Actions Workflow

The `.github/workflows/deploy-pages.yml` file contains the deployment configuration:
- Triggers on pushes to the `main` branch
- Can also be manually triggered via workflow_dispatch
- Uses official GitHub Pages actions for deployment
- Deploys the entire repository root (including index.html)

### Web Interface Features

The `index.html` file provides:
- **Client-side Excel processing** using SheetJS library
- **Drag-and-drop file upload** for easy use
- **Intelligent merging** based on Asset Code
- **No server required** - all processing happens in the browser
- **Privacy-focused** - files never leave the user's computer

### Merge Logic

The web interface implements the same merge logic as the Python script:
1. Files are matched by "Asset Code" column
2. Empty/null values are filled from other files
3. When both values exist and differ, the latest file's value is used
4. All merged data is compiled into a downloadable Excel file

## Testing Locally

You can test the web interface locally by opening `index.html` in a web browser:

```bash
# Using Python's built-in server (recommended)
python -m http.server 8000

# Or simply open the file
open index.html  # macOS
xdg-open index.html  # Linux
start index.html  # Windows
```

Then navigate to `http://localhost:8000` in your browser.

## Manual Deployment (Alternative)

If you prefer not to use GitHub Actions, you can manually enable GitHub Pages:

1. Go to repository Settings → Pages
2. Under "Build and deployment":
   - Source: Select "Deploy from a branch"
   - Branch: Select `main` and `/` (root)
3. Save the settings

The site will be built and deployed from the main branch.

## Troubleshooting

### Workflow Not Running
- Ensure GitHub Actions is enabled in the repository settings
- Check that the workflow file is in `.github/workflows/` directory
- Verify the branch name matches (default is `main`)

### 404 Error After Deployment
- Wait a few minutes after the first deployment
- Check that `index.html` exists in the repository root
- Verify the repository name matches the URL path

### Files Not Uploading in Web Interface
- Ensure files are in `.xlsx` format
- Check browser console for JavaScript errors
- Verify the SheetJS CDN link is accessible

## Security Notes

- All file processing happens client-side in the user's browser
- No data is sent to any external servers
- The SheetJS library is loaded from the official CDN
- Files are processed using the File API and never leave the user's machine

## Updates and Maintenance

The web interface will automatically update when changes are pushed to the `main` branch. No manual intervention is required for deployments.
