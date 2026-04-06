#!/bin/bash

# Script to commit and push changes for GitHub Pages deployment

echo "Staging all changes..."
git add .

echo "Committing with message 'Ready for Pages deployment'..."
git commit -m "Ready for Pages deployment"

echo "Pushing to origin main..."
git push origin main

echo "Done. Check GitHub Actions for deployment status."